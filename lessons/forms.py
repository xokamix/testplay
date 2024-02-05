from django import forms
from .models import Lesson
from django.core.exceptions import ValidationError
import dateutil.rrule as rrule
import datetime
import logging

logger = logging.getLogger(__name__)

class LessonForm(forms.ModelForm):
    recurrence_frequency = forms.ChoiceField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], required=False, label='Recurrence Frequency')
    days_of_week = forms.MultipleChoiceField(choices=[(str(i), day) for i, day in enumerate(['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'], 1)],required=False, widget=forms.CheckboxSelectMultiple(), label='Days of Week')
    
    class Meta:
        model = Lesson
        fields = [
            'title',
            'schedule',
            'duration',
            'teacher',
            'pupils',
            'group',
            'recurrence_rule',
            'end_recurrence',
            'recurrence_frequency',
            'days_of_week',
        ]

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get('recurrence_frequency')
        days = cleaned_data.get('days_of_week')
        end_recurrence = cleaned_data.get('end_recurrence')
        
        if frequency:
            if frequency == 'daily':
                cleaned_data['recurrence_rule'] = 'FREQ=DAILY'
            elif frequency == 'weekly' and days:
                cleaned_data['recurrence_rule'] = f'FREQ=WEEKLY;BYDAY={','.join(days)}'
            elif frequency == 'monthly':
                cleaned_data['recurrence_rule'] = 'FREQ=MONTHLY'
            else:
                logger.error(f'Invalid combination of recurrence frequency "{frequency}" and days of the week.')
                raise ValidationError('Invalid combination of recurrence frequency and days of the week.')
                
        if end_recurrence and end_recurrence < cleaned_data.get('schedule'):
            logger.error('End recurrence date cannot be before the schedule date.')
            raise ValidationError('End recurrence date cannot be before the schedule date.')
        try:
            rrule.rrulestr(cleaned_data.get('recurrence_rule'), dtstart=datetime.datetime.now())
        except Exception as e:
            logger.error(f'Invalid recurrence rule syntax: {e}', exc_info=True)
            raise ValidationError(f'Invalid recurrence rule syntax: {str(e)}')
        return cleaned_data

class RecurrenceForm(forms.Form):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    recurrence_frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, label="Recurrence Frequency")
    days_of_week = forms.MultipleChoiceField(choices=[(str(i), day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 1)],
                                       required=False, widget=forms.CheckboxSelectMultiple(), label='Days of Week')

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get('recurrence_frequency')
        days = cleaned_data.get('days_of_week')
        # Log and error handling
        try:
            if frequency == 'weekly' and not days:
                raise ValueError('Weekly frequency requires at least one day to be selected.')
            logger.info("RecurrenceForm cleaned successfully.")
        except ValueError as e:
            logger.error('RecurrenceForm clean method error: %s', e, exc_info=True)  # gpt_pilot_debugging_log
            raise ValidationError(f'RecurrenceForm error: {e}')
        return cleaned_data
