from django.urls import path
from django.views.generic import TemplateView

app_name = 'messaging'

urlpatterns = [
    path('inbox/', TemplateView.as_view(template_name='messaging/inbox.html'), name='inbox'),
    path('sent/', TemplateView.as_view(template_name='messaging/sent.html'), name='sent'),
    path('drafts/', TemplateView.as_view(template_name='messaging/drafts.html'), name='drafts'),
    path('compose/', TemplateView.as_view(template_name='messaging/compose.html'), name='compose'),
    path('message/<int:pk>/', TemplateView.as_view(template_name='messaging/message_detail.html'), name='message_detail'),
    # Dummy actions
    path('send-message/', TemplateView.as_view(template_name='messaging/inbox.html'), name='send_message'),
    path('send-reply/', TemplateView.as_view(template_name='messaging/inbox.html'), name='send_reply'),
    path('save-draft/', TemplateView.as_view(template_name='messaging/drafts.html'), name='save_draft'),
]