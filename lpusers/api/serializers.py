from rest_framework import serializers
from lpusers.models import Teacher, Pupil
from lessons.models import Lesson

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class PupilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pupil
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
