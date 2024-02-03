from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule_lesson, name='schedule_lesson'),
    path('calendar/', views.calendar_view, name='calendar_view'),
]