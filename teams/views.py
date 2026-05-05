"""
Views for the Teams module.

Handles displaying teams, searching, filtering by skills
and viewing detailed team information including dependencies.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Team, Skill



@login_required
def team_list(request):
    """
    Displaying all teams with search and filter capabilities.

    This view handles:
    Displaying all teams in a grid layout
    Searching by team name, description or manager username
    Filtering by skill/technology

    GET Parameters:
        q (str): Search query: searches name, description. manager username
        skill (int): Skill ID: filters teams that have this skill

    Returns:
        Rendered team_list.html with filtered teams, skills list and search query
    """
    teams = Team.objects.all()
    query = request.GET.get('q', '')

    if query:
        teams = teams.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(manager__username__icontains=query)
        )

    # Getting all skills for the filter dropdown
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
    """
    Display detailed information about a single team.
    
    This view shows:
    - Team basic information (name, department, manager, contacts)
    - Skills associated with the team (as badges)
    - Upstream dependencies (teams this team depends on)
    - Downstream dependencies (teams that depend on this team)
    - Team members list
    
    Args:
        team_id (int): Primary key of the team to display
    
    Returns:
        Rendered team_detail.html with comprehensive team data
    """

    # Getting the team or returning 404 if not found
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