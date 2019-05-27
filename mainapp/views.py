from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product, Contacts

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView


def get_hot_product():
    return Product.objects.filter(is_active=True).select_related().order_by('?').first()


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]


class IndexListView(ListView):
    model = Product
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, category__is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - main'
        return context


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.filter(is_active=True)
    if pk:
        products_list = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
            'price')
        category = get_object_or_404(ProductCategory, pk=pk, is_active=True)
    else:
        products_list = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
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
        'links_menu': links_menu,
        'category': category,
        'products_list': products_list,
        'paginated_products': paginated_products,
    }
    return render(request, 'mainapp/products_list.html', context)


class ContactsListView(ListView):
    model = Contacts
    template_name = 'mainapp/contacts.html'

    def get_queryset(self):
        return Contacts.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - contacts'
        return context


def showroom(request):
    hot_product = get_hot_product()

    context = {
        'page_title': 'Interior - showroom',
        'links_menu': ProductCategory.objects.filter(is_active=True).only('pk', 'name'),
        'product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/showroom.html', context)


def product_details(request, pk):
    context = {
        'page_title': 'Interior - product details',
        'links_menu': ProductCategory.objects.filter(is_active=True).only('pk', 'name'),
        'product': Product.objects.filter(pk=pk).select_related().first(),
    }
    return render(request, 'mainapp/product-details.html', context)
