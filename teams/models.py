"""
Models for the Teams module.
This file defines the database structure for engineering teams,
including skills, team members, dependencies and project management fields
from the Excel sheet (Jira, workstream, agile practices, etc.). 

"""

from django.db import models
from django.contrib.auth import get_user_model
# from organisation.models import Department

User = get_user_model()

class Skill(models.Model):
    """
    Represents a technical skill or technology used by teams.
    Examples: Python, Django, React, AWS, Kubernetes.
    Many-to-many relationship with Team model.
    """
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Team(models.Model):
    """
    Represents an engineering team in the broadcast company.

    Contains all fields from the original Excel sheet including:
    - Basic info: name, department, manager, description
    - Contact: email, Slack channel
    - Project management: Jira project, workstream, agile practices
    - Workload: concurrent projects count
    """

    # Basic information
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(help_text="Team mission and responsibilities")
    
    # Contact Information
    contact_email = models.EmailField()
    contact_slack = models.CharField(max_length=200, blank=True)
    code_repository = models.URLField(blank=True)

    # Skills (Many-to-Many)
    skills = models.ManyToManyField(Skill, blank=True)

    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)

    # Project Management Fields (from Excel Sheet)
    jira_project_name = models.CharField(max_length=200, blank=True, help_text="Jira project name")
    jira_board_link = models.URLField(blank=True, help_text="Link to Jira board")
    workstream = models.CharField(max_length=200, blank=True, help_text="Workstream (MF)")
    development_focus = models.TextField(blank=True, help_text="Development focus areas")
    agile_practices = models.CharField(max_length=100, blank=True, help_text="Scrum, Kanban, etc.")
    concurrent_projects = models.IntegerField(default=0, help_text="Number of concurrent projects")

    def __str__(self):
        return self.name
    
    def get_upstream_dependencies(self):
        """
        Returns teams that this team depends on.
        Used for dependency visualisation on team detail page.

        Returns:
            QuerySet of Dependency objects where this team is the target
        """
        from .models import Dependency
        return Dependency.objects.filter(to_team=self)
    
    def get_downstream_dependencies(self):
        """
        Returns teams that depend on this team.
        Used for dependency visualisation on team detail page

        Returns:
            querySet of Dependency objects where this team is the source
        """
        from .models import Dependency
        return Dependency.objects.filter(from_team=self)
    
class TeamMember(models.Model):
    """
    Junction table linking Users to Teams.
    Allows many-to-many relationship between User and Team.
    Each user can belong to multiple teams.
    Each team can have multiple members.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['team','user']

    def __str__(self):
        return f"{self.user.username} -> {self.team.name}"

class Dependency(models.Model):
    """
    Represents upstream/downstream dependency between two teams.
    Example: UI Team depends on API Team (API Team is upstream dependency of UI team)
    Uses verbose_name_plural to fix admin display spelling.
    """
    from_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='downstream')
    to_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='upstream')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Dependencies"

    def __str__(self):
        return f"{self.from_team.name} -> {self.to_team.name}"