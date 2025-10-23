from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/presentations/(?P<presentation_id>\w+)/$",
        consumers.ReactionConsumer.as_asgi(),
    ),
]
