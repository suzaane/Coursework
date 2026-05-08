from django import forms
from .models import Meeting
class MeetingForm(forms.ModelForm):
    """Form for scheduling a new meeting"""
    
    class Meta:
        model = Meeting
        fields = ['title', 'agenda', 'platform', 'meeting_link', 'meeting_date', 'start_time', 'end_time']
        widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Weekly Sprint Planning'}),
            'agenda': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What will be discussed?'}),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://zoom.us/...'}),
        }
    