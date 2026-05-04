from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/',          views.inbox,          name='inbox'),
    path('sent/',           views.sent,            name='sent'),
    path('drafts/',         views.drafts,          name='drafts'),
    path('compose/',        views.compose,         name='compose'),
    path('compose/<int:draft_id>/', views.compose, name='compose_draft'),
    path('message/<int:pk>/',       views.view_message,  name='view_message'),
    path('delete/<int:pk>/',        views.delete_message, name='delete_message'),
    path('reply/<int:pk>/',         views.reply,          name='reply'),
]
