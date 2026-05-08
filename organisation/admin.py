from django.contrib import admin
from django.http import HttpResponse
from .models import Department, DepartmentLeader, TeamType
import csv

def export_to_csv(modeladmin, request, queryset):
    """Export selected items to CSV file"""
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={model._meta.model_name}_export.csv'
    
    writer = csv.writer(response)
    # Write headers
    headers = [field.name for field in model._meta.fields]
    writer.writerow(headers)
    
    # Write data
    for obj in queryset:
        row = [str(getattr(obj, field.name)) for field in model._meta.fields]
        writer.writerow(row)
    
    return response

export_to_csv.short_description = "Export selected items to CSV"

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialisation', 'get_team_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'specialisation']
    actions = [export_to_csv]  # Make sure this line exists
    
    def get_team_count(self, obj):
        return obj.get_team_count()
    get_team_count.short_description = 'Teams'

@admin.register(DepartmentLeader)
class DepartmentLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'email']
    search_fields = ['name', 'department__name']
    actions = [export_to_csv]

@admin.register(TeamType)
class TeamTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    actions = [export_to_csv]