"""
Admin configuration for Teams module.

Registers models with Django's built-in admin panel 
to allow easy data management through the web interface.
"""

from django.contrib import admin
from .models import Team, TeamMember, Dependency, Skill

# Registering each model to appear in the Django admin panel
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Dependency)
admin.site.register(Skill)
