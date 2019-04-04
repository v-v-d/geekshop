from django.shortcuts import render
from .models import ProductCategory, Product


def main(request):
    # products_list = [product for i, product in enumerate(Product.objects.all()) if i != 1]   # Hardcode detected
    # products_list = [product for product in Product.objects.all()]
    products_list = Product.objects.all()
    context = {
        'page_title': 'Interior - main',
        'products': products_list,
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    # Product.object.get(pk=pk)
    context = {
        'page_title': 'Interior - products'
    }
    return render(request, 'mainapp/products.html', context)


def contacts(request):
    context = {
        'page_title': 'Interior - contacts'
    }
    return render(request, 'mainapp/contacts.html', context)


def product_details(request):
    links_menu = [
        {'name': 'All'},
        {'name': 'HOME'},
        {'name': 'OFFICE'},
        {'name': 'FURNITURE'},
        {'name': 'MODERN'},
        {'name': 'CLASSIC'},
    ]
    context = {
        'page_title': 'Interior - product details',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/product-details.html', context)
