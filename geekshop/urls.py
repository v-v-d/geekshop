"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
import mainapp.views as mainapp
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    url(r'^', include('mainapp.urls', namespace='main')),
    url(r'^admin_custom/', include('adminapp.urls', namespace='admin_custom')),
    url(r'^auth/', include('authapp.urls', namespace='auth')),
    url(r'^basket/', include('basketapp.urls', namespace='basket')),
    url(r'^', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^order/', include('ordersapp.urls', namespace='order')),
    # url(r'^__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
