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

VIEWS_UNITY_NAME_UNITY_ = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'model', views.model, name='model'),
    url(r'history', views.history, name='history'),
    url(r'real', views.real, name='real'),

    url(r'temp', views.GetArduino, name='temp'),
    url(r'dht', views.GetMaxdata, name='dht'),
    url(r'arduino', views.arduino, name='arduino'),
    url(r'unity', views.unity, name="unity"),

    url(r'chart', views.chart, name="chart"),
    url(r'GetDate', views.GetDate, name="GetDate"),
    url(r'header', views.header, name="header"),
    url(r'GetOutlier',views.GetOutlier,name="GetOutlier"),
    url(r'SetOutlier',views.SetOutlier,name="SetOutlier"),

]

urlpatterns = VIEWS_UNITY_NAME_UNITY_
