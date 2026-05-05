"""
URL configuration for the Tean module.

Maps URL patterns to their corresponding view functions.
Uses app_name for reverse URL lookups in templates.
"""

from django.urls import path
from .import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
]