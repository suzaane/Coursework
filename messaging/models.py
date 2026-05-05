from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('draft', 'Draft'),
    ]

    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE,
        null=True, blank=True
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_read = models.BooleanField(default=False)

    # Soft-delete: both sides can delete independently
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_recipient = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.status.upper()}] {self.subject} | {self.sender} to {self.recipient}"
