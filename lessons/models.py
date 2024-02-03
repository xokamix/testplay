from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Teacher, Pupil

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

    def __str__(self):
        return self.title
