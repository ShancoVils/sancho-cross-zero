from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import appdata.routing
 
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            appdata.routing.websocket_urlpatterns
        )
    ),
})