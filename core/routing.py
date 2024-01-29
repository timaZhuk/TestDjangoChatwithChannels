#AuthMiddlewareStack hook up user when user register
#to chat channels
from channels.auth import AuthMiddlewareStack
# utilise routing
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing 

#alternative to urlpatterns. ws for requests in WebSocket
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    #wrap up our rrequest (authentication into AuthMiddlewareStack )
    'websocket':AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
    ),
})