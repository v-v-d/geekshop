from django.db import transaction
from django.forms import inlineformset_factory

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory, Contacts
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm, ContactsEditForm, OrderEditForm

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'админка/пользователи'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'пользователи/создание'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'пользователи/редактирование'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'пользователи/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(ShopUser, pk=kwargs['pk'])
        user.is_active = False
        user.save()
        return HttpResponseRedirect(self.success_url)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    ordering = ['-is_active', 'name']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'админка/категории'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'категории/создание'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'категории/редактирование'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'категории/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        category = get_object_or_404(ProductCategory, pk=kwargs['pk'])
        category.is_active = False
        category.save()
        return HttpResponseRedirect(self.success_url)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    ordering = ['-is_active', 'name']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'админка/продукты'
        return context

    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs['pk']).select_related('category')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'продукт/создание'
        # context['category_pk'] = self.kwargs['pk']
        context['category_name'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk']).name
        return context

    def get_success_url(self):
        return reverse_lazy('admin_custom:products', kwargs=self.kwargs)

    def get_initial(self):
        self.initial['category'] = ProductCategory.objects.filter(pk=self.kwargs['pk']).first()
        return self.initial


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductReadDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'продукт/подробнее'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'продукт/редактирование'
        return context

    def get_initial(self):
        self.initial['category'] = get_object_or_404(Product, pk=self.kwargs['pk']).category.pk
        return self.initial

    def get_success_url(self):
        category_pk = get_object_or_404(Product, pk=self.kwargs['pk']).category.pk
        return reverse_lazy('admin_custom:products', kwargs={'pk': category_pk})


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = 'продукт/удаление'
        return context

    def get_success_url(self):
        category_pk = get_object_or_404(Product, pk=self.kwargs['pk']).category.pk
        return reverse_lazy('admin_custom:products', kwargs={'pk': category_pk})

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        product.is_active = False
        product.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ContactsListView(ListView):
    model = Contacts
    template_name = 'adminapp/contacts.html'
    ordering = ['-is_active', 'name']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(ContactsListView, self).get_context_data(**kwargs)
        context['page_title'] = 'админка/контакты'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ContactsCreateView(CreateView):
    model = Contacts
    template_name = 'adminapp/contact_update.html'
    form_class = ContactsEditForm
    success_url = reverse_lazy('admin_custom:contacts')

    def get_context_data(self, **kwargs):
        context = super(ContactsCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'контакты/создание'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ContactsUpdateView(UpdateView):
    model = Contacts
    form_class = ContactsEditForm
    template_name = 'adminapp/contact_update.html'
    success_url = reverse_lazy('admin_custom:contacts')

    def get_context_data(self, **kwargs):
        context = super(ContactsUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'контакты/редактирование'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ContactsDeleteView(DeleteView):
    model = Contacts
    template_name = 'adminapp/contact_delete.html'
    success_url = reverse_lazy('admin_custom:contacts')

    def get_context_data(self, **kwargs):
        context = super(ContactsDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = 'контакты/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        contact = get_object_or_404(Contacts, pk=kwargs['pk'])
        contact.is_active = False
        contact.save()
        return HttpResponseRedirect(self.success_url)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'adminapp/order_list.html'
    ordering = ['-is_active', '-created']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'админка/заказы'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    template_name = 'adminapp/order_form.html'
    form_class = OrderEditForm
    success_url = reverse_lazy('admin_custom:orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - order create'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=10)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            formset = OrderFormSet()

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

        if self.object.get_total_cost() == 0 or self.object.status == 'CNC':
            self.object.delete()

        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class OrderReadDetailView(DetailView):
    model = Order
    template_name = 'adminapp/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'заказ/подробнее'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderEditForm
    template_name = 'adminapp/order_form.html'
    success_url = reverse_lazy('admin_custom:orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'заказы/редактирование'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            context['orderitems'] = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['orderitems'] = OrderFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0 or self.object.status == 'CNC':
            self.object.delete()

        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'adminapp/order_confirm_delete.html'
    success_url = reverse_lazy('admin_custom:orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'заказы/удаление'
        return context
