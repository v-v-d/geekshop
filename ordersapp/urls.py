from django.conf.urls import url
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    url(r'^$', ordersapp.OrderList.as_view(), name='order_list'),
    url(r'^forming/complete/(?P<pk>\d+)/$', ordersapp.order_forming_complete, name='order_forming_complete'),
    url(r'^create/$', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    url(r'^read/(?P<pk>\d+)/$', ordersapp.OrderRead.as_view(), name='order_read'),
    url(r'^update/(?P<pk>\d+)/$', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    url(r'^update/product/(?P<pk>\d+)/$', ordersapp.get_product_price, name='order_product_price'),
    url(r'^delete/(?P<pk>\d+)/$', ordersapp.OrderDelete.as_view(), name='order_delete'),
]
