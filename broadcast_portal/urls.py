from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('schedule/', include('schedule.urls', namespace='schedule')),
    path('', include('schedule.urls', namespace='schedule')),
]
