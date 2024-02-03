from django.urls import path, include
from rest_framework import routers
from users.api.views import CustomAuthToken
from lessons.api.views import TeacherViewSet, PupilViewSet, LessonViewSet

router = routers.DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'pupils', PupilViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]

urlpatterns += router.urls
