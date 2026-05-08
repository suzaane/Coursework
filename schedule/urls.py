from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('monthly/', views.monthly_view, name='monthly'),
    path('weekly/', views.weekly_view, name='weekly'),
    path('upcoming/', views.upcoming, name='upcoming'),
    path('schedule/', views.new_meeting, name='schedule_meeting'),  
    path('new/', views.new_meeting, name='new_meeting'),  
    path('cancel/<int:meeting_id>/', views.cancel_meeting, name='cancel_meeting'),
]