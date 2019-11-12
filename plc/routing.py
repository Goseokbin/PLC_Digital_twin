from django.conf.urls import url
from . import connection

websocket_urlpatterns = [
    url(r'^ws/unity/plcmodel', connection.plcConsumer),
]
