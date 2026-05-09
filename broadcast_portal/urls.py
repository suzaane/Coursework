from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

dashboard_view = login_required(
    TemplateView.as_view(template_name='dashboard.html'),
    login_url='/accounts/login/'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('teams/', include('teams.urls')),
    path('organisation/', include('organisation.urls')),
    path('messages/', include('messaging.urls')),
    path('schedule/', include('schedule.urls')),
    path('', dashboard_view, name='dashboard'),
]