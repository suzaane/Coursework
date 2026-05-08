from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Department, TeamType, DepartmentLeader

def dashboard(request):
    """Dashboard showing summary statistics"""
    from teams.models import Dependency
    
    context = {
        'department_count': Department.objects.count(),
        'teamtype_count': TeamType.objects.count(),
        'leader_count': DepartmentLeader.objects.count(),
        'dependency_count': Dependency.objects.count(),
        'departments': Department.objects.all(),
        'team_types': TeamType.objects.all(),
    }
    return render(request, 'organisation/dashboard.html', context)


def department_list(request):
    """Show all departments with optional search."""
    query = request.GET.get('q', '')
    departments = Department.objects.all()
    if query:
        departments = departments.filter(
            Q(name__icontains=query) | Q(specialisation__icontains=query)
        )
    return render(request, 'organisation/department_list.html', {
        'departments': departments,
        'query': query,
    })


def department_detail(request, pk):
    """Show a single department with its leader and teams."""
    department = get_object_or_404(Department, pk=pk)
    teams = []
    
    try:
        from teams.models import Team
        teams = Team.objects.filter(department=department)
    except ImportError:
        pass
    
    return render(request, 'organisation/department_detail.html', {
        'department': department,
        'teams': teams,
    })


def teamtype_list(request):
    """Show all team types."""
    team_types = TeamType.objects.all()
    return render(request, 'organisation/teamtype_list.html', {
        'team_types': team_types,
    })


def dependency_list(request):
    """Show all upstream/downstream dependencies."""
    direction = request.GET.get('direction', '')
    dependencies = []
    
    try:
        from teams.models import Dependency
        dependencies = Dependency.objects.all()
    except ImportError:
        pass
    
    return render(request, 'organisation/dependency_list.html', {
        'dependencies': dependencies,
        'selected_direction': direction,
    })


def org_chart(request):
    """Show the organisation chart — departments and their teams."""
    departments = Department.objects.prefetch_related('leader').all()
    
    teams_by_department = {}
    try:
        from teams.models import Team
        teams = Team.objects.select_related('department').all()
        for team in teams:
            if team.department:
                dept_id = team.department.id
                if dept_id not in teams_by_department:
                    teams_by_department[dept_id] = []
                teams_by_department[dept_id].append(team)
    except ImportError:
        pass
    
    return render(request, 'organisation/org_chart.html', {
        'departments': departments,
        'teams_by_department': teams_by_department,
    })