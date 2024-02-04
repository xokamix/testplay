from django.db import models
from django.utils.translation import gettext_lazy as _
from lpusers.models import Teacher, Pupil
import datetime
import logging

logger = logging.getLogger(__name__)

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    schedule = models.DateTimeField()
    duration = models.DurationField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    pupils = models.ManyToManyField(Pupil)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    recurrence_rule = models.CharField(max_length=255, blank=True, null=True, help_text="iCalendar RRULE format")
    end_recurrence = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title

class LessonOccurrence(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='occurrences')
    occurrence_date = models.DateTimeField()
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        try:
            return f'{self.lesson.title} on {self.occurrence_date.strftime("%Y-%m-%d %H:%M")}'
        except Exception as e:
            logger.error("Error formatting LessonOccurrence string representation: %s", str(e), exc_info=True)
            return f'{self.lesson.title} occurrence error'