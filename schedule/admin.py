from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'organiser', 'meeting_date', 'start_time', 'platform', 'is_cancelled']
    list_filter = ['platform', 'is_cancelled', 'meeting_date']
    search_fields = ['title', 'agenda', 'organiser__username']
    date_hierarchy = 'meeting_date' 

    