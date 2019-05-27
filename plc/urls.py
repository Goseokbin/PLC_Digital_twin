"""gdproject URL Configuration

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
from django.conf.urls import url
from plc import views
from plc.views import *

app_name='plc'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'model', views.model, name='model'),
    url(r'history', views.history, name='history'),
    url(r'real', views.real, name='real'),
    url(r'temp',views.GetArduino2, name='temp'),
    url(r'chart',views.GetArduino, name='chart'),
    url(r'dht',views.dht, name='dht'),
    url(r'arduino',views.arduino, name='arduino'),
    url(r'^GetArduino', views.arduino,name='GetArduino'),
    url(r'barchart', views.barchart, name='barchart'),

]