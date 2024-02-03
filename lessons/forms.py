from django import forms
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'schedule', 'duration', 'teacher', 'pupils', 'group']
    
    def clean_schedule(self):
        schedule = self.cleaned_data.get('schedule')
        # Implement your logic here to check for scheduling conflicts
        return schedule
