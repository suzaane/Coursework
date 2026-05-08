from django.urls import path
from . import views

app_name = 'organisation'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('team-types/', views.teamtype_list, name='teamtype_list'),
    path('dependencies/', views.dependency_list, name='dependency_list'),
    path('org-chart/', views.org_chart, name='org_chart'),
]