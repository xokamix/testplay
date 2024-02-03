from rest_framework import viewsets
from users.api.serializers import TeacherSerializer, PupilSerializer
from lessons.models import Lesson
from users.models import Teacher, Pupil
from users.api.serializers import LessonSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class PupilViewSet(viewsets.ModelViewSet):
    queryset = Pupil.objects.all()
    serializer_class = PupilSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
