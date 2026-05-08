from django.contrib import admin
from .models import Department, DepartmentLeader, TeamType

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialisation', 'created_at']
    search_fields = ['name', 'specialisation']


@admin.register(DepartmentLeader)
class DepartmentLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'email']
    search_fields = ['name', 'department__name']


@admin.register(TeamType)
class TeamTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']