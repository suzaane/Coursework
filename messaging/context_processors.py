from .models import Message


def unread_message_count(request):
    """
    Makes 'unread_count' available in ALL templates automatically.
    This powers the red badge on the Messages sidebar link.
    """
    if request.user.is_authenticated:
        count = Message.objects.filter(
            recipient=request.user,
            status='sent',
            is_read=False,
            deleted_by_recipient=False
        ).count()
        return {'unread_count': count}
    return {'unread_count': 0}

