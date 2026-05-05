from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q
from django.http import Http404
from .models import Message
from .forms import ComposeMessageForm


# ─── INBOX ────────────────────────────────────────────────────────────────────

@login_required
def inbox(request):
    """Show all received sent messages that haven't been deleted by recipient."""
    msgs = Message.objects.filter(
        recipient=request.user,
        status='sent',
        deleted_by_recipient=False
    )
    unread_count = msgs.filter(is_read=False).count()
    return render(request, 'messaging/inbox.html', {
        'messages_list': msgs,
        'unread_count': unread_count,
        'active_tab': 'inbox',
    })


# ─── SENT ─────────────────────────────────────────────────────────────────────

@login_required
def sent(request):
    """Show all messages sent by the current user."""
    msgs = Message.objects.filter(
        sender=request.user,
        status='sent',
        deleted_by_sender=False
    )
    return render(request, 'messaging/sent.html', {
        'messages_list': msgs,
        'active_tab': 'sent',
    })


# ─── DRAFTS ───────────────────────────────────────────────────────────────────

@login_required
def drafts(request):
    """Show all draft messages saved by the current user."""
    msgs = Message.objects.filter(
        sender=request.user,
        status='draft'
    )
    return render(request, 'messaging/drafts.html', {
        'messages_list': msgs,
        'active_tab': 'drafts',
    })


# ─── COMPOSE / SEND / SAVE DRAFT ──────────────────────────────────────────────

@login_required
def compose(request, draft_id=None):
    """
    Compose a new message or edit an existing draft.
    draft_id: if provided, loads that draft for editing.
    """
    instance = None
    if draft_id:
        instance = get_object_or_404(Message, pk=draft_id, sender=request.user, status='draft')

    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, instance=instance, current_user=request.user)
        action = request.POST.get('action')  # 'send' or 'draft'

        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user

            if action == 'send':
                if not msg.recipient:
                    form.add_error('recipient', 'A recipient is required to send a message.')
                else:
                    msg.status = 'sent'
                    msg.save()
                    django_messages.success(request, 'Message sent successfully.')
                    return redirect('messaging:sent')

            elif action == 'draft':
                msg.status = 'draft'
                msg.save()
                django_messages.success(request, 'Draft saved.')
                return redirect('messaging:drafts')

    else:
        form = ComposeMessageForm(instance=instance, current_user=request.user)

    return render(request, 'messaging/compose.html', {
        'form': form,
        'draft_id': draft_id,
        'active_tab': 'compose',
    })


# ─── VIEW SINGLE MESSAGE ──────────────────────────────────────────────────────

@login_required
def view_message(request, pk):
    """
    View a single message. Only the sender (for drafts/sent) or
    the recipient (for inbox) can view it.
    """
    msg = get_object_or_404(Message, pk=pk)

    # Security: only sender or recipient may view
    if request.user != msg.sender and request.user != msg.recipient:
        raise Http404

    # Mark as read if recipient is viewing
    if request.user == msg.recipient and not msg.is_read:
        msg.is_read = True
        msg.save()

    return render(request, 'messaging/message_detail.html', {
        'msg': msg,
    })


# ─── DELETE MESSAGE ───────────────────────────────────────────────────────────

@login_required
def delete_message(request, pk):
    """Soft-delete: marks message as deleted for the requesting user."""
    msg = get_object_or_404(Message, pk=pk)

    if request.user == msg.sender:
        msg.deleted_by_sender = True
        msg.save()
        django_messages.success(request, 'Message deleted from Sent.')
        return redirect('messaging:sent')
    elif request.user == msg.recipient:
        msg.deleted_by_recipient = True
        msg.save()
        django_messages.success(request, 'Message deleted from Inbox.')
        return redirect('messaging:inbox')
    else:
        raise Http404


# ─── REPLY ────────────────────────────────────────────────────────────────────

@login_required
def reply(request, pk):
    """Pre-fill compose form with recipient and subject for a reply."""
    original = get_object_or_404(Message, pk=pk, recipient=request.user)
    form = ComposeMessageForm(
        current_user=request.user,
        initial={
            'recipient': original.sender,
            'subject': f"Re: {original.subject}",
        }
    )
    return render(request, 'messaging/compose.html', {
        'form': form,
        'replying_to': original,
        'active_tab': 'inbox',
    })
