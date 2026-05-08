from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib.auth.models import User, Group
from .models import Department, TeamType, DepartmentLeader

class BroadcastAdminSite(AdminSite):
    site_header = "Broadcast Portal - Engineering Department"
    site_title = "Broadcast Admin"
    index_title = "Admin Dashboard"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.custom_dashboard), name='custom_dashboard'),
            path('reports/', self.admin_view(self.reports_view), name='reports'),
            path('statistics/', self.admin_view(self.statistics_view), name='statistics'),
        ]
        return custom_urls + urls
    
    def custom_dashboard(self, request):
        context = {
            'department_count': Department.objects.count(),
            'teamtype_count': TeamType.objects.count(),
            'leader_count': DepartmentLeader.objects.count(),
            'user_count': User.objects.count(),
            'group_count': Group.objects.count(),
            'recent_departments': Department.objects.all()[:5],
            'recent_teamtypes': TeamType.objects.all()[:5],
        }
        return TemplateResponse(request, "admin/custom_dashboard.html", context)
    
    def reports_view(self, request):
        context = {
            'departments': Department.objects.all(),
            'teamtypes': TeamType.objects.all(),
        }
        return TemplateResponse(request, "admin/reports.html", context)
    
    def statistics_view(self, request):
        context = {
            'department_count': Department.objects.count(),
            'teamtype_count': TeamType.objects.count(),
            'leader_count': DepartmentLeader.objects.count(),
        }
        return TemplateResponse(request, "admin/statistics.html", context)

admin_site = BroadcastAdminSite(name='broadcast_admin')