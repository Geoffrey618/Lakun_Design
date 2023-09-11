from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat import consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', consumer.ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/(?P<username>\w+)/$', consumer.NotificationConsumer.as_asgi()),

]
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})
