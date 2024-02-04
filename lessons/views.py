from django.shortcuts import render, redirect
from .models import Lesson, Teacher, Pupil, Group
from .forms import LessonForm, RecurrenceForm
from django.db.models import Q
import logging
from django.contrib import messages

logger = logging.getLogger(__name__)

def schedule_lesson(request):
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST)
        recurrence_form = RecurrenceForm(request.POST)
        if lesson_form.is_valid() and recurrence_form.is_valid():
            lesson = lesson_form.save(commit=False)
            recurrence_data = recurrence_form.cleaned_data
            lesson.recurrence_rule = recurrence_data.get('recurrence_rule', '')
            try:
                lesson.save()
                logger.info('Lesson and recurrence scheduled successfully.')
            except Exception as e:
                logger.error(f'Error saving lesson and recurrence: {e}', exc_info=True)
            return redirect('calendar_view')
    else:
        lesson_form = LessonForm()
        recurrence_form = RecurrenceForm()

    return render(request, 'lessons/schedule_lesson.html', {'lesson_form': lesson_form, 'recurrence_form': recurrence_form})

def calendar_view(request):
    try:
        lessons = Lesson.objects.all()
        filter_by = request.GET.get('filter_by')
        filter_id = request.GET.get('id')

        if filter_by == 'teacher' and filter_id:
            lessons = lessons.filter(teacher__id=filter_id)
            logger.info(f"Filtered lessons by teacher with ID: {filter_id}")
        elif filter_by == 'pupil' and filter_id:
            lessons = lessons.filter(pupils__id=filter_id)
            logger.info(f"Filtered lessons by pupil with ID: {filter_id}")
        elif filter_by == 'group' and filter_id:
            lessons = lessons.filter(group__id=filter_id)
            logger.info(f"Filtered lessons by group with ID: {filter_id}")

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
        logger.error(f"Error loading calendar view: {str(e)}", exc_info=True)

def schedule_recurring_lesson(request):
    try:
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Recurring lesson scheduled successfully.')
                logger.info('Recurring lesson scheduled successfully.')
                return redirect('calendar_view')
            else:
                for error in form.errors:
                    messages.error(request, f'Error in form field {error}: {form.errors[error]}')
                    logger.error(f'Error in form field {error}: {form.errors[error]}')
        else:
            form = LessonForm()
        return render(request, 'lessons/schedule_lesson.html', {'form': form})
    except Exception as e:
        logger.error('Error scheduling recurring lesson: %s', str(e), exc_info=True)
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return redirect('schedule_lesson')