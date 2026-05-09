from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# Dashboard – only accessible when logged in
dashboard_view = login_required(
    TemplateView.as_view(template_name='dashboard.html'),
    login_url='/accounts/login/'
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('accounts/', include('accounts.urls')),

    # Student apps — uncomment when they provide urls.py
    # path('teams/', include('teams.urls')),
    # path('organisation/', include('organisation.urls')),
    # path('schedule/', include('schedule.urls')),

    # Messaging – your working app
    path('messages/', include('messaging.urls')),

    # Home / Dashboard
    path('', dashboard_view, name='dashboard'),
]