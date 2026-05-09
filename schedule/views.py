from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from calendar import monthcalendar
from datetime import datetime, timedelta, date
from .models import Meeting
from .forms import MeetingForm

def dashboard(request):
    """Dashboard view showing upcoming meetings"""
    today = date.today()
    upcoming_meetings = Meeting.objects.filter(
        meeting_date__gte=today,
        is_cancelled=False
    ).order_by('meeting_date', 'start_time')[:10]
    
    return render(request, 'schedule/dashboard.html', {
        'upcoming_meetings': upcoming_meetings,
        'active_tab': 'dashboard'
    })

def monthly_view(request):
    """Display meetings in a monthly calendar view"""
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    meetings = Meeting.objects.filter(
        meeting_date__gte=start_date,
        meeting_date__lt=end_date,
        is_cancelled=False
    )
    
    calendar_grid = monthcalendar(year, month)
    
    meetings_by_date = {}
    for meeting in meetings:
        meetings_by_date[meeting.meeting_date] = meetings_by_date.get(meeting.meeting_date, []) + [meeting]
    
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    # Use monthly.html 
    return render(request, 'schedule/monthly.html', {
        'calendar_grid': calendar_grid,
        'meetings_by_date': meetings_by_date,
        'current_year': year,
        'current_month': month,
        'month_name': start_date.strftime('%B'),
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'active_tab': 'monthly'
    })

def weekly_view(request):
    """Display meetings in a weekly view"""
    today = date.today()
    year = int(request.GET.get('year', today.year))
    week = int(request.GET.get('week', today.isocalendar()[1]))
    
    start_of_week = date.fromisocalendar(year, week, 1)
    end_of_week = start_of_week + timedelta(days=6)
    
    meetings = Meeting.objects.filter(
        meeting_date__gte=start_of_week,
        meeting_date__lte=end_of_week,
        is_cancelled=False
    ).order_by('meeting_date', 'start_time')
    
    days = []
    for i in range(7):
        current_date = start_of_week + timedelta(days=i)
        day_meetings = [m for m in meetings if m.meeting_date == current_date]
        days.append({
            'date': current_date,
            'day_name': current_date.strftime('%A'),
            'meetings': day_meetings
        })
    
    prev_week = week - 1
    prev_year = year
    if prev_week < 1:
        prev_week = 52
        prev_year = year - 1
    
    next_week = week + 1
    next_year = year
    if next_week > 52:
        next_week = 1
        next_year = year + 1
    
    # Using weekly.html
    return render(request, 'schedule/weekly.html', {
        'days': days,
        'current_year': year,
        'current_week': week,
        'prev_year': prev_year,
        'prev_week': prev_week,
        'next_year': next_year,
        'next_week': next_week,
        'active_tab': 'weekly'
    })

def upcoming(request):
    """Display upcoming meetings list"""
    today = date.today()
    meetings = Meeting.objects.filter(
        meeting_date__gte=today,
        is_cancelled=False
    ).order_by('meeting_date', 'start_time')[:20]
    
    # Use upcoming.html 
    return render(request, 'schedule/upcoming.html', {
        'meetings': meetings,
        'active_tab': 'upcoming'
    })

def new_meeting(request):
    """Schedule a new meeting"""
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            # Creating a default user
            from django.contrib.auth.models import User
            default_user, created = User.objects.get_or_create(username='testuser')
            if created:
                default_user.set_password('testpass123')
                default_user.save()
            meeting.organiser = default_user
            meeting.save()
            messages.success(request, f'Meeting "{meeting.title}" scheduled successfully!')
            return redirect('schedule:dashboard')
    else:
        form = MeetingForm()
    
    # Use schedule_meeting.html
    return render(request, 'schedule/schedule_meeting.html', {'form': form})

def cancel_meeting(request, meeting_id):
    """Cancel a scheduled meeting"""
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    if request.method == 'POST':
        meeting.is_cancelled = True
        meeting.save()
        messages.success(request, f'Meeting "{meeting.title}" has been cancelled.')
        return redirect('schedule:upcoming')
    
    return render(request, 'schedule/cancel_meeting.html', {'meeting': meeting})