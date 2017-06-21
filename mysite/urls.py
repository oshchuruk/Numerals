"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from myapp import views
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/(?P<inp_number>.+)/$', views.hello, name='hello'),
    url(r'^hello_cro/(?P<inp_number>.+)/$', views.hello_cro, name='hello_cro'),
    url(r'^insert/', views.insert, name='insert'),
    url(r'^insert_cro/', views.insert_cro, name='insert_cro'),
    url(r'^$', TemplateView.as_view(template_name='start_ukr.html')),
    url(r'^cro/', TemplateView.as_view(template_name='start_cro.html')),
]
