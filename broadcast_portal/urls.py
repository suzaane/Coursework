from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('teams/', include('teams.urls')),
    path('schedule/', include('schedule.urls')),
    path('organisation/', include('organisation.urls')),
]