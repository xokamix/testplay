from django.contrib import admin
from .models import Lesson, Group
import logging

# Set up logging
logger = logging.getLogger(__name__)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'schedule', 'duration', 'teacher')
    list_filter = ('teacher', 'group')
    search_fields = ('title', 'teacher__user__username', 'group__name')
    filter_horizontal = ('pupils',)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
            logger.info(f"Lesson '{obj.title}' saved successfully.")
        except Exception as e:
            logger.error("Error saving Lesson model: %s", str(e), exc_info=True)
            raise e

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
            logger.info(f"Group '{obj.name}' saved successfully.")
        except Exception as e:
            logger.error("Error saving Group model: %s", str(e), exc_info=True)
            raise e

try:
    admin.site.register(Lesson, LessonAdmin)
    admin.site.register(Group, GroupAdmin)
    logger.info("Lesson and Group models registered with the admin site.")
except Exception as e:
    logger.error("Error registering Lesson and Group models with the admin site: %s", str(e), exc_info=True)