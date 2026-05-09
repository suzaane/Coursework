from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Department, TeamType, DepartmentLeader

def dashboard(request):
    dependency_count = 0
    team_count = 0
    try:
        from teams.models import Team, Dependency
        team_count = Team.objects.count()
        dependency_count = Dependency.objects.count()
    except ImportError:
        pass
    
    context = {
        'department_count': Department.objects.count(),
        'teamtype_count': TeamType.objects.count(),
        'leader_count': DepartmentLeader.objects.count(),
        'dependency_count': dependency_count,
        'team_count': team_count,
        'departments': Department.objects.all(),
        'team_types': TeamType.objects.all(),
    }
    return render(request, 'organisation/dashboard.html', context)

def department_list(request):
    query = request.GET.get('q', '')
    departments = Department.objects.all()
    if query:
        departments = departments.filter(
            Q(name__icontains=query) | Q(specialisation__icontains=query)
        )
    for dept in departments:
        dept.team_count = dept.get_team_count()
    return render(request, 'organisation/department_list.html', {
        'departments': departments,
        'query': query,
    })

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    teams = department.get_teams()
    return render(request, 'organisation/department_detail.html', {
        'department': department,
        'teams': teams,
        'team_count': len(teams),
    })

def teamtype_list(request):
    team_types = TeamType.objects.all()
    return render(request, 'organisation/teamtype_list.html', {
        'team_types': team_types,
    })

def dependency_list(request):
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
    departments = Department.objects.prefetch_related('leader').all()
    org_data = []
    total_teams = 0
    for dept in departments:
        teams = dept.get_teams()
        team_count = len(teams)
        total_teams += team_count
        org_data.append({
            'department': dept,
            'teams': teams,
            'team_count': team_count
        })
    dependency_count = 0
    try:
        from teams.models import Dependency
        dependency_count = Dependency.objects.count()
    except ImportError:
        pass
    return render(request, 'organisation/org_chart.html', {
        'org_data': org_data,
        'total_departments': departments.count(),
        'total_teams': total_teams,
        'dependency_count': dependency_count,
    })

# NEW: Statistics page
def admin_statistics(request):
    context = {
        'department_count': Department.objects.count(),
        'teamtype_count': TeamType.objects.count(),
        'leader_count': DepartmentLeader.objects.count(),
    }
    return render(request, 'admin/statistics.html', context)

# NEW: Reports page
def admin_reports(request):
    context = {
        'departments': Department.objects.all(),
        'teamtypes': TeamType.objects.all(),
    }
    return render(request, 'admin/reports.html', context)