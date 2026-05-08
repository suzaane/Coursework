from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Meeting(models.Model):
    """
    Model for scheduled meetings.
    Each meeting is tied to an organiser and optionally a team.
    """
    PLATFORM_CHOICES = [
        ('zoom', 'Zoom'),
        ('teams', 'Microsoft Teams'),
        ('slack', 'Slack'),
        ('google_meet', 'Google Meet'),
        ('in_person', 'In Person'),
        ('other', 'Other'),
    ]
    
    
    organiser = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='organised_meetings'
    )
    
   
    # Meeting details
    title = models.CharField(max_length=200)
    agenda = models.TextField(blank=True, help_text="Meeting agenda or description")
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='teams')
    meeting_link = models.URLField(blank=True, help_text="Join link if applicable")
    
    # Date and time
    meeting_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    
    # Status
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['meeting_date', 'start_time']
    
    def __str__(self):
        return f"{self.title} - {self.meeting_date} at {self.start_time}"
    
    def is_upcoming(self):
        """Return True if meeting is today or in future"""
        from datetime import date
        return self.meeting_date >= date.today() and not self.is_cancelled