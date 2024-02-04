from rest_framework import viewsets
from lpusers.api.serializers import TeacherSerializer, PupilSerializer
from lessons.models import Lesson
from lpusers.models import Teacher, Pupil
from lpusers.api.serializers import LessonSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime
from dateutil.rrule import rrulestr
import logging

logger = logging.getLogger(__name__)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class PupilViewSet(viewsets.ModelViewSet):
    queryset = Pupil.objects.all()
    serializer_class = PupilSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recurring_lessons(request):
    try:
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        start_date_parsed = datetime.datetime.fromisoformat(start_date) if start_date else datetime.date.today()
        end_date_parsed = datetime.datetime.fromisoformat(end_date) if end_date else start_date_parsed + datetime.timedelta(days=30)

        lessons = Lesson.objects.filter(schedule__lte=end_date_parsed, end_recurrence__gte=start_date_parsed)
        lessons_data = []
        for lesson in lessons:
            if lesson.recurrence_rule:
                try:
                    recurrence_rule = rrulestr(lesson.recurrence_rule, dtstart=lesson.schedule)
                    for occurrence in recurrence_rule.between(start_date_parsed, end_date_parsed, inc=True):
                        lessons_data.append({
                            "id": lesson.id,
                            "title": lesson.title,
                            "schedule": occurrence.strftime('%Y-%m-%d %H:%M:%S'),
                            "duration": str(lesson.duration),
                            "teacher": lesson.teacher.user.username,
                            "start_date": occurrence,
                            "end_date": (occurrence + lesson.duration).strftime('%Y-%m-%d %H:%M:%S')
                        })
                except Exception as e:
                    logger.error("Error processing recurrence for lesson %s: %s", lesson.id, str(e), exc_info=True)
    except Exception as e:
        logger.error("Error fetching recurring lessons: %s", str(e), exc_info=True)
        return Response(status=500, data={"message": "Internal server error"})
    logger.info("Recurring lessons fetched successfully.")
    return Response(lessons_data)