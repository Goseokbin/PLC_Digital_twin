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
    url(r'history', views.history, name='history'),
    url(r'base', views.base, name='base'),
    url(r'index2', views.index2, name='index2'),

    url(r'dht', views.GetMaxdata, name='dht'),
    url(r'arduino', views.arduino, name='arduino'),
    url(r'unity', views.unity, name="unity"),

    url(r'GetDate', views.GetDate, name="GetDate"),
    url(r'GetOutlier',views.GetOutlier,name="GetOutlier"),
    url(r'OutlierHistory',views.OutlierHistory,name="OutlierHistory"),
    url(r'SetOutlier',views.SetOutlier,name="SetOutlier"),
    url(r'sendplcoutlier',views.sendplcoutlier,name="sendplcoutlier"),
    # url(r'setPLC',views.setPLC,name="setPLC"),
    url(r'getPLC',views.getPLC,name="getPLC"),
    url(r'webgl',views.webgl,name="webgl"),


]

urlpatterns = VIEWS_UNITY_NAME_UNITY_
