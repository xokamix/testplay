from django.contrib import admin
from django.urls import path, include
import logging

logger = logging.getLogger(__name__)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('letsplay.api_urls')),
]

logger.info("URL patterns for LetsPlay project configured successfully.")