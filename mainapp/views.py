from django.shortcuts import render


def main(request):
    context = {
        'page_title': 'Interior - main'
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
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
