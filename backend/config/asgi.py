"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from presentations import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Django ASGIアプリケーションを初期化（importより前に必要）
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # 通常のHTTPリクエスト
        "websocket": AuthMiddlewareStack(  # WebSocket接続
            URLRouter(routing.websocket_urlpatterns)  # WebSocketのルーティング
        ),
    }
)
