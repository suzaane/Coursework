"""
Custom User model for the Broadcast Portal.

Extends Django's AbstractUser to add role selection and additional fields.
This replaces the default auth.User model.

"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model with role selection.
    
    Extends Django's built-in User with:
    - Role choices (Engineer, Team Leader, Department Leader, Senior Manager)
    - Phone number field
    - Department field
    
    The role field determines what permissions the user has in the application.
    """
    ROLE_CHOICES = (
        ('engineer', 'Engineer'),
        ('team_leader', 'Team Leader'),
        ('dept_leader', 'Department Leader'),
        ('senior_manager', 'Senior Manager'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='engineer')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.username

