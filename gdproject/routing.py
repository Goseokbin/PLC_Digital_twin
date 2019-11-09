from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import plc.routing

# channel open
application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(
        URLRouter(
            plc.routing.websocket_urlpatterns
        )
    ),
})