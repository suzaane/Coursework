from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Team, Skill



@login_required
def team_list(request):
    teams = Team.objects.all()
    query = request.GET.get('q', '')

    if query:
        teams = teams.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(manager__username__icontains=query)
        )


    skills = Skill.objects.all()
    skill_id = request.GET.get('skill')
    if skill_id:
        teams = teams.filter(skills_id=skill_id)

    return render(request, 'teams/team_list.html',{
        'teams':teams,
        'skills': skills,
        'query': query,
    })

@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    members = team.members.select_related('user').all()
    upstream = team.get_upstream_dependencies()
    downstream = team.get_downstream_dependencies()
    skills = team.skills.all()

    return render(request, 'teams/team_detail.html', {
        'team': team,
        'members': members,
        'upstream': upstream,
        'downstream': downstream,
        'skills': skills,
    })