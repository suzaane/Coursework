from django.urls import path, include
from organisation.admin_dashboard import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('organisation/', include('organisation.urls')),
]