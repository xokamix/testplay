from django.contrib import admin
from .models import Teacher, Pupil, Administrator
import logging

# Configuring logging
logger = logging.getLogger(__name__)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subjects_taught')
    search_fields = ('user__username', 'user__email', 'subjects_taught')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        logger.info(f"Teacher {obj.user.username} saved successfully.")

class PupilAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        logger.info(f"Pupil {obj.user.username} saved successfully.")

class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        logger.info(f"Administrator {obj.user.username} saved successfully.")

try:
    admin.site.register(Teacher, TeacherAdmin)
    admin.site.register(Pupil, PupilAdmin)
    admin.site.register(Administrator, AdministratorAdmin)
    logger.info("Teachers, Pupils, and Administrators successfully registered in the admin site.")
except Exception as e:
    logger.error("An error occurred while registering models in the admin site.", exc_info=True)