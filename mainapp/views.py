from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product, Contacts
from basketapp.models import Basket

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView


# def get_user_basket(user):
#     return Basket.objects.filter(user=user) if user.is_authenticated else []


# def get_common_context(request):
#     common_context = {
#         'products_total_quantity': Basket.objects.all()[0].get_products_total_quantity_by_user,
#         'products_total_price': Basket.objects.all()[0].get_products_total_price_by_user,
#     }
#     return common_context
#
#     # common_context = {}
#     # if get_user_basket(request.user):
#     #     common_context = {
#     #         'basket': get_user_basket(request.user),
#     #         'products_total_quantity': get_user_basket(request.user)[0].get_products_total_quantity_by_user,
#     #         'products_total_price': get_user_basket(request.user)[0].get_products_total_price_by_user,
#     #     }
#     # return common_context


def get_hot_product():
    return Product.objects.filter(is_active=True).order_by('?').first()


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]


# def main(request):
#     context = {
#         'page_title': 'Interior - main',
#         'products': Product.objects.filter(is_active=True, category__is_active=True),
#         # **get_common_context(request),
#     }
#     return render(request, 'mainapp/index.html', context)


class IndexListView(ListView):
    model = Product
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, category__is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Interior - main'
        return context


# class ProductsListView(ListView):
#     model = ProductCategory
#     template_name = 'mainapp/products_list.html'
#     # paginate_by = 3
#
#     def get_queryset(self):
#         if self.kwargs:
#             return get_object_or_404(ProductCategory, pk=self.kwargs['pk']).product_set.filter(is_active=True).order_by('price')
#         else:
#             return get_object_or_404(ProductCategory).product_set.filter(is_active=True).order_by('price')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = 'Interior - products'


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.filter(is_active=True)
    if pk:
        products_list = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
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


# def contacts(request):
#
#     context = {
#         'page_title': 'Interior - contacts',
#         'contacts': Contacts.objects.filter(is_active=True),
#         # **get_common_context(request),
#     }
#     return render(request, 'mainapp/contacts.html', context)


# class ShowroomListView(ListView):
#     model = ProductCategory
#     template_name = 'mainapp/showroom.html'
#     hot_product = get_hot_product()
#
#     def get_queryset(self):
#         return ProductCategory.objects.filter(is_active=True)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = 'Interior - showroom'
#         context['hot_product'] = self.hot_product
#         context['same_products'] = get_same_products(self.hot_product)
#         context['category_pk'] = self.hot_product.category.pk


def showroom(request):
    hot_product = get_hot_product()

    context = {
        'page_title': 'Interior - showroom',
        'links_menu': ProductCategory.objects.filter(is_active=True),
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
        'category_pk': hot_product.category.pk,
        # **get_common_context(request),
    }
    return render(request, 'mainapp/showroom.html', context)


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'mainapp/product-details.html'
#
#     def get_queryset(self):
#         pass
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = 'Interior - product details'


def product_details(request, pk):
    context = {
        'page_title': 'Interior - product details',
        'links_menu': ProductCategory.objects.filter(is_active=True),
        'detailed_product': get_object_or_404(Product, pk=pk),
        'category_pk': get_object_or_404(Product, pk=pk).category.pk,
        # **get_common_context(request),
    }
    return render(request, 'mainapp/product-details.html', context)
