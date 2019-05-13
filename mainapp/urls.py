from django.conf.urls import url
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    url(r'^$', mainapp.IndexListView.as_view(), name='index'),
    # url(r'^products/all/$', mainapp.ProductsListView.as_view(), name='products'),
    url(r'^products/all/$', mainapp.products, name='products'),
    url(r'^products/all/(?P<page>\d+)/$', mainapp.products, name='catalog'),
    url(r'^products/category/(?P<pk>\d+)/$', mainapp.products, name='category'),
    url(r'^products/category/(?P<pk>\d+)/(?P<page>\d+)/$', mainapp.products, name='page'),
    url(r'^showroom/', mainapp.showroom, name='showroom'),
    url(r'^product-details/(?P<pk>\d+)', mainapp.product_details, name='product-details'),
    url(r'^contacts/', mainapp.ContactsListView.as_view(), name='contacts'),
]
