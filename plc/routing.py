from django.conf.urls import url
from . import comsumer

websocket_urlpatterns = [
    url(r'ws/unity', comsumer.websocket_connect),
]
