from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'recipient', 'is_read', 'is_draft', 'created_at']
    list_filter = ['is_read', 'is_draft', 'created_at']
    search_fields = ['subject', 'body', 'sender__username', 'recipient__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Sender/Recipient', {'fields': ('sender', 'recipient')}),
        ('Message Content', {'fields': ('subject', 'body')}),
        ('Status', {'fields': ('is_read', 'is_draft')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )