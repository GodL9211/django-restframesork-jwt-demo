#! -*-conding=: UTF-8 -*-
# 2023/5/4 15:07
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from app01 import routing
from django.core.asgi import get_asgi_application


urlpatterns = []
urlpatterns += routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    # 'websocket': AuthMiddlewareStack( # 使用AuthMiddlewareStack，后续在视图类中可以取出self.scope，相当于request对象
    #     URLRouter(
    #         routing.websocket_urlpatterns# 指明路由文件是django_websocket/routing.py,类似于路由分发
    #     )
    # ),
    'websocket': URLRouter(
        routing.websocket_urlpatterns  # 指明路由文件是django_websocket/routing.py,类似于路由分发
    ),
    "http": get_asgi_application(),
})
