from django.shortcuts import render, get_object_or_404

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm

# class-based view
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'title': 'админка/пользователи',
#         'objects': ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     }
#     return render(request, 'adminapp/users.html', context)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_custom:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': 'пользователи/создание',
#         'form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', context)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_custom:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': 'пользователи/редактирование',
#         'update_form': edit_form
#     }
#     return render(request, 'adminapp/user_update.html', context)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_custom:users'))
#
#     context = {
#         'title': 'пользователи/удаление',
#         'user_to_delete': user
#     }
#     return render(request, 'adminapp/user_delete.html', context)
#
#
# def categories(request):
#     context = {
#         'title': 'админка/категории',
#         'objects': ProductCategory.objects.all()
#     }
#     return render(request, 'adminapp/categories.html', context)


# def category_create(request):
#     pass


# def category_update(request):
#     pass
#
#
# def category_delete(request):
#     pass
#


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


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data(**kwargs)
        context['page_title'] = 'админка/категории'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'категории/создание'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    fields = '__all__'
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


# @method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
# class ProductsListView(ListView):
#     model = Product
#     template_name = 'adminapp/products.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductsListView, self).get_context_data(**kwargs)
#         context['page_title'] = 'админка/продукты'
#         return context
#
#
# @method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
# class ProductCreateView(CreateView):
#     model = Product
#     template_name = 'adminapp/product_update.html'
#     fields = '__all__'
#     success_url = reverse_lazy('admin_custom:products')
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductCreateView, self).get_context_data(**kwargs)
#         context['page_title'] = 'продукт/создание'
#         return context


def products(request, pk):
    context = {
        'title': 'админка/продукт',
        'category': get_object_or_404(ProductCategory, pk=pk),
        'object_list': Product.objects.filter(category__pk=pk).order_by('name'),
    }
    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
