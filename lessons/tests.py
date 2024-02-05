from django.test import TestCase
from .models import Lesson, Teacher, Pupil, Group
from django.contrib.auth.models import User
from .forms import LessonForm
import datetime

class LessonFormTestCase(TestCase):
    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher', password='testpass123')
        self.pupil_user = User.objects.create_user(username='pupil', password='testpass123')
        self.teacher = Teacher.objects.create(user=self.teacher_user, subjects_taught='Math')
        self.pupil = Pupil.objects.create(user=self.pupil_user)
        self.group = Group.objects.create(name='Music Fundamentals')

    def test_daily_recurrence_rule(self):
        form_data = {
            'title': 'Daily Music Lesson',
            'schedule': datetime.datetime.now(),
            'duration': datetime.timedelta(hours=1),
            'teacher': self.teacher.id,
            'pupils': [self.pupil.id],
            'group': self.group.id,
            'recurrence_frequency': 'daily',
            'end_recurrence': datetime.datetime.now() + datetime.timedelta(days=10)
        }
        form = LessonForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['recurrence_rule'], 'FREQ=DAILY')
    
    def test_weekly_recurrence_rule_valid(self):
        form_data = {
            'title': 'Weekly Music Lesson',
            'schedule': datetime.datetime.now(),
            'duration': datetime.timedelta(hours=1),
            'teacher': self.teacher.id,
            'pupils': [self.pupil.id],
            'group': self.group.id,
            'recurrence_frequency': 'weekly',
            'days_of_week': ['1', '3'],
            'end_recurrence': datetime.datetime.now() + datetime.timedelta(days=30)
        }
        form = LessonForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['recurrence_rule'], 'FREQ=WEEKLY;BYDAY=1,3')
    
    def test_weekly_recurrence_rule_invalid(self):
        form_data = {
            'title': 'Invalid Weekly Music Lesson',
            'schedule': datetime.datetime.now(),
            'duration': datetime.timedelta(hours=1),
            'teacher': self.teacher.id,
            'pupils': [self.pupil.id],
            'group': self.group.id,
            'recurrence_frequency': 'weekly',
            'end_recurrence': datetime.datetime.now() + datetime.timedelta(days=30)
        }
        form = LessonForm(data=form_data)
        self.assertFalse(form.is_valid())
