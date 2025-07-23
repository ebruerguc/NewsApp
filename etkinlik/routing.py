from django.urls import re_path
from etkinlik import consumers

websocket_urlpatterns= [
    re_path(r'ws/duyurular/$', consumers.DuyuruConsumer.as_asgi()),
    re_path(r'ws/haberler/$', consumers.HaberConsumer.as_asgi()),
]