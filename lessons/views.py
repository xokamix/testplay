from django.shortcuts import render, redirect
from .models import Lesson, Teacher, Pupil, Group
from .forms import LessonForm
from django.db.models import Q
import logging

def schedule_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            logging.info("Lesson scheduled successfully.")
            return redirect('lessons_list')
    else:
        form = LessonForm()
    return render(request, 'lessons/schedule_lesson.html', {'form': form})

def calendar_view(request):
    try:
        lessons = Lesson.objects.all()
        filter_by = request.GET.get('filter_by')
        filter_id = request.GET.get('id')

        if filter_by == 'teacher' and filter_id:
            lessons = lessons.filter(teacher__id=filter_id)
            logging.info("Filtered lessons by teacher with ID: %s", filter_id)
        elif filter_by == 'pupil' and filter_id:
            lessons = lessons.filter(pupils__id=filter_id)
            logging.info("Filtered lessons by pupil with ID: %s", filter_id)
        elif filter_by == 'group' and filter_id:
            lessons = lessons.filter(group__id=filter_id)
            logging.info("Filtered lessons by group with ID: %s", filter_id)

        teachers = Teacher.objects.all()
        pupils = Pupil.objects.all()
        groups = Group.objects.all()

        return render(request, 'lessons/calendar_view.html', {
            'lessons': lessons,
            'teachers': teachers,
            'pupils': pupils,
            'groups': groups,
        })
    except Exception as e:
        logging.error("Error loading calendar view: %s", str(e), exc_info=True)