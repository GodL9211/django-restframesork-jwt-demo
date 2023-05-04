#! -*-conding=: UTF-8 -*-
# 2023/5/4 14:39
from django.urls import re_path
from app01 import consumers

websocket_urlpatterns = [
    re_path('ws/webssh/(?P<host>.*)/(?P<username>\w+)/(?P<password>\w+)', consumers.SSHConsumer.as_asgi()),
]
