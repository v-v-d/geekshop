import adminapp.views as adminapp
from django.conf.urls import url

app_name = 'adminapp'

urlpatterns = [
    # url(r'^users/create/$', adminapp.user_create, name='user_create'),
    # url(r'^users/read/$', adminapp.users, name='users'),
    # url(r'^users/update/(?P<pk>\d+)/$', adminapp.user_update, name='user_update'),
    # url(r'^users/delete/(?P<pk>\d+)/$', adminapp.user_delete, name='user_delete'),
    # url(r'^categories/create/$', adminapp.category_create, name='category_create'),
    # url(r'^categories/read/$', adminapp.categories, name='categories'),
    # url(r'^categories/update/(?P<pk>\d+)/$', adminapp.category_update, name='category_update'),
    # url(r'^categories/delete/(?P<pk>\d+)/$', adminapp.category_delete, name='category_delete'),
    url(r'^products/create/category/(?P<pk>\d+)/$', adminapp.product_create, name='product_create'),
    url(r'^products/read/category/(?P<pk>\d+)/$', adminapp.products, name='products'),
    # url(r'^products/read/(?P<pk>\d+)/$', adminapp.product_read, name='product_read'),
    # url(r'^products/update/(?P<pk>\d+)/$', adminapp.product_update, name='product_update'),
    # url(r'^products/delete/(?P<pk>\d+)/$', adminapp.product_delete, name='product_delete'),

    url(r'^users/create/$', adminapp.UsersCreateView.as_view(), name='user_create'),
    url(r'^users/read/$', adminapp.UsersListView.as_view(), name='users'),
    url(r'^users/update/(?P<pk>\d+)/$', adminapp.UsersUpdateView.as_view(), name='user_update'),
    url(r'^users/delete/(?P<pk>\d+)/$', adminapp.UsersDeleteView.as_view(), name='user_delete'),

    url(r'^categories/create/$', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    url(r'^categories/read/$', adminapp.ProductCategoryListView.as_view(), name='categories'),
    url(r'^categories/update/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    url(r'^categories/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    # url(r'^products/create/category/(?P<pk>\d+)/$', adminapp.ProductCategoryCreateView.as_view(), name='product_create'),
    # url(r'^products/read/category/(?P<pk>\d+)/$', adminapp.ProductsListView.as_view(), name='products'),
    url(r'^products/read/(?P<pk>\d+)/$', adminapp.product_read, name='product_read'),
    url(r'^products/update/(?P<pk>\d+)/$', adminapp.product_update, name='product_update'),
    url(r'^products/delete/(?P<pk>\d+)/$', adminapp.product_delete, name='product_delete'),
]
