from django.contrib import admin
from .models import Team, TeamMember, Dependency, Skill

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Dependency)
admin.site.register(Skill)


