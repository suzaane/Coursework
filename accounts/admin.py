# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'department', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'department']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'department')}),
    )

admin.site.register(User, CustomUserAdmin)
