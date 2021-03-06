import adminapp.views as adminapp
from django.conf.urls import url

app_name = 'adminapp'

urlpatterns = [
    url(r'^users/create/$', adminapp.UsersCreateView.as_view(), name='user_create'),
    url(r'^users/read/$', adminapp.UsersListView.as_view(), name='users'),
    url(r'^users/update/(?P<pk>\d+)/$', adminapp.UsersUpdateView.as_view(), name='user_update'),
    url(r'^users/delete/(?P<pk>\d+)/$', adminapp.UsersDeleteView.as_view(), name='user_delete'),

    url(r'^categories/create/$', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    url(r'^categories/read/$', adminapp.ProductCategoryListView.as_view(), name='categories'),
    url(r'^categories/update/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    url(r'^categories/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    url(r'^products/create/category/(?P<pk>\d+)/$', adminapp.ProductCreateView.as_view(), name='product_create'),
    url(r'^products/read/category/(?P<pk>\d+)/$', adminapp.ProductsListView.as_view(), name='products'),
    url(r'^products/read/(?P<pk>\d+)/$', adminapp.ProductReadDetailView.as_view(), name='product_read'),
    url(r'^products/update/(?P<pk>\d+)/$', adminapp.ProductUpdateView.as_view(), name='product_update'),
    url(r'^products/delete/(?P<pk>\d+)/$', adminapp.ProductDeleteView.as_view(), name='product_delete'),

    url(r'^contacts/create/$', adminapp.ContactsCreateView.as_view(), name='contact_create'),
    url(r'^contacts/read/$', adminapp.ContactsListView.as_view(), name='contacts'),
    url(r'^contacts/update/(?P<pk>\d+)/$', adminapp.ContactsUpdateView.as_view(), name='contact_update'),
    url(r'^contacts/delete/(?P<pk>\d+)/$', adminapp.ContactsDeleteView.as_view(), name='contact_delete'),

    url(r'^order/create/$', adminapp.OrderCreateView.as_view(), name='order_create'),
    url(r'^order/read/$', adminapp.OrderListView.as_view(), name='orders'),
    url(r'^order/read/(?P<pk>\d+)/$', adminapp.OrderReadDetailView.as_view(), name='order_read'),
    url(r'^order/update/(?P<pk>\d+)/$', adminapp.OrderUpdateView.as_view(), name='order_update'),
    url(r'^order/delete/(?P<pk>\d+)/$', adminapp.OrderDeleteView.as_view(), name='order_delete'),
]
