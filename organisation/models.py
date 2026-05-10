from django.db import models
# from teams.models import Team

class Department(models.Model):
    """Represents a broadcast company department."""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    specialisation = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_team_count(self):
        """Returns the number of teams in this department"""
        try:
            from teams.models import Team
            return Team.objects.filter(department=self.name).count()
        except ImportError:
            return 0
    
    def get_teams(self):
        """Returns all teams in this department"""
        try:
            from teams.models import Team
            return Team.objects.filter(department=self.name)
        except ImportError:
            return []

    class Meta:
        ordering = ['name']


class DepartmentLeader(models.Model):
    """Tracks the leader of each department."""
    department = models.OneToOneField(
        Department, on_delete=models.CASCADE, related_name='leader'
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.department.name})"


class TeamType(models.Model):
    """Categorises teams by type e.g. Platform, Product, QA."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']