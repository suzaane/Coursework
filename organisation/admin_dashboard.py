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
            path('statistics/', self.admin_view(self.statistics_view), name='statistics'),
            path('reports/', self.admin_view(self.reports_view), name='reports'),
        ]
        return custom_urls + urls
    
    def statistics_view(self, request):
        context = {
            'department_count': Department.objects.count(),
            'teamtype_count': TeamType.objects.count(),
            'leader_count': DepartmentLeader.objects.count(),
        }
        return TemplateResponse(request, "admin/statistics.html", context)
    
    def reports_view(self, request):
        context = {
            'departments': Department.objects.all(),
            'teamtypes': TeamType.objects.all(),
        }
        return TemplateResponse(request, "admin/reports.html", context)

# Use this admin site
admin_site = BroadcastAdminSite(name='broadcast_admin')