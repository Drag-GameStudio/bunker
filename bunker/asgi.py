"""
ASGI config for bunker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import game.routing
import lobby
import lobby.routing
import game

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bunker.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack( URLRouter(
            lobby.routing.websocket_urlpatterns + game.routing.websocket_urlpatterns
        ))
    })
