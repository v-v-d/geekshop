from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse


# def get_user_basket(user):
#     return Basket.objects.filter(user=user) if user.is_authenticated else []
#
#
# def get_common_context(request):
#     common_context = {}
#     if get_user_basket(request.user):
#         common_context = {
#             'basket': get_user_basket(request.user),
#             'products_total_quantity': get_user_basket(request.user)[0].get_products_total_quantity_by_user,
#             'products_total_price': get_user_basket(request.user)[0].get_products_total_price_by_user,
#         }
#     return common_context


@login_required
def basket(request):
    context = {
        'page_title': 'Interior - shopping cart',
        'basket_items': Basket.objects.filter(user=request.user).order_by('product__category'),
        # **get_common_context(request),
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse(viewname='product-details', args=[pk]))

    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
