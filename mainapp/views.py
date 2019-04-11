from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket


def get_user_basket(request):
    user_basket = []
    if request.user.is_authenticated:
        user_basket = Basket.objects.filter(user=request.user)
    return user_basket


def get_common_context(request):
    common_context = {}
    if get_user_basket(request):
        common_context = {
            'basket': get_user_basket(request),
            'products_total_quantity': get_user_basket(request)[0].get_products_total_quantity_by_user,
            'products_total_price': get_user_basket(request)[0].get_products_total_price_by_user,
        }
    return common_context


def main(request):
    products_list = Product.objects.all()[:4]
    context = {
        'page_title': 'Interior - main',
        'products': products_list,
        **get_common_context(request),
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    page_title = 'Interior - products'

    links_menu = ProductCategory.objects.all()
    if pk:
        if pk == '0':
            products = Product.objects.all().order_by('price')
            category = {'name': 'ALL'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'page_title': page_title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            **get_common_context(request),
        }

        return render(request, 'mainapp/products_list.html', context)

    same_products = Product.objects.all()[3: 5]
    context = {
        'page_title': page_title,
        'links_menu': links_menu,
        'same_products': same_products,
        **get_common_context(request),
    }

    return render(request, 'mainapp/products.html', context)


def contacts(request):
    context = {
        'page_title': 'Interior - contacts',
        **get_common_context(request),
    }
    return render(request, 'mainapp/contacts.html', context)


def product_details(request):
    links_menu = ProductCategory.objects.all()

    context = {
        'page_title': 'Interior - product details',
        'links_menu': links_menu,
        **get_common_context(request),
    }
    return render(request, 'mainapp/product-details.html', context)
