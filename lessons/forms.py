from django import forms
from .models import Lesson
from django.core.exceptions import ValidationError
import dateutil.rrule as rrule
import datetime
import logging

logger = logging.getLogger(__name__)

class LessonForm(forms.ModelForm):
    weekly_recurrence = forms.MultipleChoiceField(choices=[(str(i), f'Every {day}') for i, day in enumerate(['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'], 1)],
                                                  required=False, widget=forms.CheckboxSelectMultiple(), label='Weekly Recurrence')

    class Meta:
        model = Lesson
        fields = ['title', 'schedule', 'duration', 'teacher', 'pupils', 'group', 'recurrence_rule', 'end_recurrence']
    
    def clean(self):
        cleaned_data = super().clean()
        weekly = cleaned_data.get('weekly_recurrence')
        
        if weekly:
            try:
                recurrence_rule = 'FREQ=WEEKLY;BYDAY=' + ','.join(weekly)
                rrule.rrulestr(recurrence_rule, dtstart=datetime.datetime.now())
                cleaned_data['recurrence_rule'] = recurrence_rule
            except Exception as e:
                logger.error("Invalid weekly recurrence rule syntax: %s", str(e), exc_info=True)  # gpt_pilot_debugging_log
                raise ValidationError(f"Invalid weekly recurrence rule syntax: {str(e)}")
        
        # Additional validation for schedule and recurrence_rule fields here
        schedule = cleaned_data.get('schedule')
        end_recurrence = cleaned_data.get('end_recurrence')
        if schedule and end_recurrence and end_recurrence < schedule:
            logger.error("End recurrence date cannot be before the schedule date.")  # gpt_pilot_debugging_log
            raise ValidationError("End recurrence date cannot be before the schedule date.")
        
        return cleaned_data

    def clean_schedule(self):
        schedule = self.cleaned_data.get('schedule')
        # Custom logic for checking scheduling conflicts
        logger.info("Validating schedule...")  # gpt_pilot_debugging_log
        return schedule