from django.core.paginator import Paginator
from django.shortcuts import HttpResponse
from django.views import View

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm

# class-based view
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['page_title'] = 'админка/пользователи'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_update.html'
    # fields = '__all__'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(UsersCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'пользователи/создание'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    # fields = '__all__'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(UsersUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'пользователи/редактирование'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(UsersDeleteView, self).get_context_data(**kwargs)
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

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data(**kwargs)
        context['page_title'] = 'админка/категории'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'категории/создание'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'категории/редактирование'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryDeleteView, self).get_context_data(**kwargs)
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
    # paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['page_title'] = 'админка/продукты'
        context['category_pk'] = self.kwargs['pk']
        context['category_name'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk']).name
        return context

    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs['pk'])


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'продукт/создание'
        context['category_pk'] = self.kwargs['pk']
        context['category_name'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk']).name
        return context

    def get_initial(self):
        self.initial['category'] = self.kwargs['pk']
        return self.initial

    def get_success_url(self):
        return reverse_lazy('admin_custom:products', kwargs=self.kwargs)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductReadDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super(ProductReadDetailView, self).get_context_data(**kwargs)
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
        context['category_pk'] = get_object_or_404(Product, pk=self.kwargs['pk']).category.pk
        context['category_name'] = get_object_or_404(Product, pk=self.kwargs['pk']).category.name
        return context

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


