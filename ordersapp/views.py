from django.db.models import F
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from django.http import JsonResponse


@method_decorator(login_required(), name='dispatch')
class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - orders'
        return context


@method_decorator(login_required(), name='dispatch')
class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - order create'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.basket.all().select_related()
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            self.request.user.basket.all().delete()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0 or self.object.status == 'CNC':
            self.object.delete()

        return super().form_valid(form)


@method_decorator(login_required(), name='dispatch')
class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - order'
        return context


@method_decorator(login_required(), name='dispatch')
class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - order update'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            context['orderitems'] = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object, queryset=self.object.orderitems.select_related())
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            context['orderitems'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0 or self.object.status == 'CNC':
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - order delete'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('order:order_list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        return JsonResponse({'price': product.price}) if product else JsonResponse({'price': 0})


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity = F('quantity') + sender.get_item(instance.pk).quantity - instance.quantity
    else:
        instance.product.quantity = F('quantity') + instance.quantity
    # instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity if instance.pk else instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity = F('quantity') + instance.quantity
    # instance.product.quantity += instance.quantity
    instance.product.save()
