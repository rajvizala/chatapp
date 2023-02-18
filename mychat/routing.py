# chat/routing.py
from django.urls import re_path #relative path

from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/socket-server', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/socket-server/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]