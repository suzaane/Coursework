from django.db import models
from django.contrib.auth import get_user_model
# from organisation.models import Department

User = get_user_model()

class Skill(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    # department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    contact_email = models.EmailField()
    contact_slack = models.CharField(max_length=200, blank=True)
    code_repository = models.URLField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.name
    
    def get_upstream_dependencies(self):
        from .models import Dependency
        return Dependency.objects.filter(to_team=self)
    
    def get_downstream_dependencies(self):
        from .models import Dependency
        return Dependency.objects.filter(from_team=self)
    
class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['team','user']

    def __str__(self):
        return f"{self.user.username} -> {self.team.name}"

class Dependency(models.Model):
    from_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='downstream')
    to_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='upstream')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Dependencies"

    def __str__(self):
        return f"{self.from_team.name} -> {self.to_team.name}"