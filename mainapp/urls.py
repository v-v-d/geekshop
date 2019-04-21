from django.conf.urls import url
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    url(r'^$', mainapp.products, name='index'),
    url(r'^category/(?P<pk>\d+)/$', mainapp.products, name='category'),
]
