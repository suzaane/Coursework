# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model with role selection"""
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

# Create your models here.
