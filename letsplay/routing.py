from django.urls import re_path
from .consumers import LessonConsumer
import logging

logger = logging.getLogger(__name__)

websocket_urlpatterns = [
    re_path(r'ws/lessons/(?P<lesson_id>\w+)/$', LessonConsumer.as_asgi(), name='lesson_updates'),
]

logger.info("WebSocket URL patterns configured.")