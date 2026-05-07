from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# Dashboard view – accessible only when logged in
dashboard_view = login_required(
    TemplateView.as_view(template_name='dashboard.html'),
    login_url='/accounts/login/'
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (accounts)
    path('accounts/', include('accounts.urls')),

    # Other apps – commented out until they provide urls.py
    # path('teams/', include('teams.urls')),
    # path('organisation/', include('organisation.urls')),
    # path('schedule/', include('schedule.urls')),

    # Messaging – your app
    path('messages/', include('messaging.urls')),

    # Dashboard home
    path('', dashboard_view, name='dashboard'),
]