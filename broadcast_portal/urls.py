from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),  # Temporarily disabled - fix User model conflict
    path('teams/', include('teams.urls')),
    path('organisation/', include('organisation.urls')),
]