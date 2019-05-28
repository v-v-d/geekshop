from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from mainapp.models import ProductCategory, Product, Contacts

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page, never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    return get_products().order_by('?').first()
    # return Product.objects.filter(is_active=True).select_related().order_by('?').first()


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]


class IndexListView(ListView):
    model = Product
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        return get_products()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - main'
        return context


# @cache_page(3600)
def products(request, pk=None, page=1):
    if pk:
        products_list = get_products_in_category_orederd_by_price(pk)
        category = get_category(pk)
    else:
        products_list = get_products_orederd_by_price()
        category = {'name': 'ALL'}

    products_paginator = Paginator(products_list, 3)

    try:
        paginated_products = products_paginator.page(page)
    except PageNotAnInteger:
        paginated_products = products_paginator.page(1)
    except EmptyPage:
        paginated_products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'Interior - products',
        'links_menu': get_links_menu(),
        'category': category,
        'products_list': products_list,
        'paginated_products': paginated_products,
    }

    if request.is_ajax():
        result = render_to_string('mainapp/includes/inc__products_list_content.html', context=context, request=request)
        return JsonResponse({'result': result})
    else:
        return render(request, 'mainapp/products_list.html', context)


class ContactsListView(ListView):
    model = Contacts
    template_name = 'mainapp/contacts.html'

    def get_queryset(self):
        if settings.LOW_CACHE:
            key = f'locations'
            locations = cache.get(key)
            if locations is None:
                locations = Contacts.objects.filter(is_active=True).select_related()
                cache.set(key, locations)
            return locations
        else:
            return Contacts.objects.filter(is_active=True).select_related()
        # return Contacts.objects.filter(is_active=True).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - contacts'
        return context


def showroom(request):
    hot_product = get_hot_product()

    context = {
        'page_title': 'Interior - showroom',
        'links_menu': get_links_menu(),
        'product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/showroom.html', context)


def product_details(request, pk):
    context = {
        'page_title': 'Interior - product details',
        'links_menu': get_links_menu(),
        'product': get_product(pk),
    }
    return render(request, 'mainapp/product-details.html', context)
