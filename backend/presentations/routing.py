from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/presentations/<str:presentation_id>/", consumers.ReactionConsumer.as_asgi()),
]
