from .models import Message

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(
            recipient=request.user,
            is_draft=False,
            is_read=False,
            deleted_by_recipient=False
        ).count()
        return {'unread_count': count}
    return {'unread_count': 0}