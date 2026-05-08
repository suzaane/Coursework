from .models import Message

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(
            recipient=request.user,
            status='sent',
            is_read=False,
            deleted_by_recipient=False
        ).count()
        return {'unread_count': count}
    # If the user is not authenticated, return 0 directly – do NOT use count here
    return {'unread_count': 0}