from django.urls import path
from . import views
from .views import schedule_recurring_lesson

urlpatterns = [
    path('schedule/', views.schedule_lesson, name='schedule_lesson'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('schedule-recurring/', schedule_recurring_lesson, name='schedule_recurring_lesson'),
]