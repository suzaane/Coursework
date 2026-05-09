
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Message


class MessageModelTest(TestCase):
    """Tests for the Message model itself."""

    def setUp(self):
        self.user1 = User.objects.create_user('alice', 'alice@test.com', 'pass1234')
        self.user2 = User.objects.create_user('bob',   'bob@test.com',   'pass1234')

    def test_create_sent_message(self):
        msg = Message.objects.create(
            sender=self.user1, recipient=self.user2,
            subject='Hello', body='Test body', status='sent'
        )
        self.assertEqual(msg.status, 'sent')
        self.assertFalse(msg.is_read)
        self.assertEqual(str(msg), '[SENT] Hello | alice to bob')

    def test_create_draft(self):
        msg = Message.objects.create(
            sender=self.user1, subject='Draft msg', body='Draft body', status='draft'
        )
        self.assertEqual(msg.status, 'draft')
        self.assertIsNone(msg.recipient)

    def test_soft_delete_by_sender(self):
        msg = Message.objects.create(
            sender=self.user1, recipient=self.user2,
            subject='Del test', body='body', status='sent'
        )
        msg.deleted_by_sender = True
        msg.save()
        visible = Message.objects.filter(sender=self.user1, deleted_by_sender=False)
        self.assertNotIn(msg, visible)

    def test_soft_delete_by_recipient(self):
        msg = Message.objects.create(
            sender=self.user1, recipient=self.user2,
            subject='Del test 2', body='body', status='sent'
        )
        msg.deleted_by_recipient = True
        msg.save()
        visible = Message.objects.filter(recipient=self.user2, deleted_by_recipient=False)
        self.assertNotIn(msg, visible)


class InboxViewTest(TestCase):
    """Tests for inbox, sent, drafts views."""

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user('alice', 'alice@test.com', 'pass1234')
        self.user2 = User.objects.create_user('bob',   'bob@test.com',   'pass1234')

    # ── Auth tests ───────────────────────────────────────────────────────────

    def test_inbox_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_sent_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('messaging:sent'))
        self.assertEqual(response.status_code, 302)

    def test_drafts_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('messaging:drafts'))
        self.assertEqual(response.status_code, 302)

    def test_compose_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('messaging:compose'))
        self.assertEqual(response.status_code, 302)

    # ── Inbox tests ──────────────────────────────────────────────────────────

    def test_inbox_loads_for_logged_in_user(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inbox')

    def test_inbox_shows_received_messages_only(self):
        msg = Message.objects.create(
            sender=self.user2, recipient=self.user1,
            subject='Hi Alice', body='body', status='sent'
        )
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertContains(response, 'Hi Alice')

    def test_inbox_does_not_show_drafts(self):
        Message.objects.create(
            sender=self.user2, recipient=self.user1,
            subject='Draft msg', body='body', status='draft'
        )
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertNotContains(response, 'Draft msg')

    def test_inbox_does_not_show_deleted_messages(self):
        msg = Message.objects.create(
            sender=self.user2, recipient=self.user1,
            subject='Deleted msg', body='body', status='sent',
            deleted_by_recipient=True
        )
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertNotContains(response, 'Deleted msg')

    # ── Sent tests ───────────────────────────────────────────────────────────

    def test_sent_shows_sent_messages(self):
        Message.objects.create(
            sender=self.user1, recipient=self.user2,
            subject='Sent by Alice', body='body', status='sent'
        )
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('messaging:sent'))
        self.assertContains(response, 'Sent by Alice')

    # ── Drafts tests ─────────────────────────────────────────────────────────

    def test_drafts_shows_draft_messages(self):
        Message.objects.create(
            sender=self.user1, subject='My Draft', body='body', status='draft'
        )
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('messaging:drafts'))
        self.assertContains(response, 'My Draft')

    # ── Compose / Send tests ─────────────────────────────────────────────────

    def test_send_message_successfully(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.post(reverse('messaging:compose'), {
            'recipient': self.user2.pk,
            'subject': 'Test Send',
            'body': 'Hello Bob',
            'action': 'send',
        })
        self.assertEqual(response.status_code, 302)
        msg = Message.objects.get(subject='Test Send')
        self.assertEqual(msg.status, 'sent')
        self.assertEqual(msg.sender, self.user1)
        self.assertEqual(msg.recipient, self.user2)

    def test_save_as_draft(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.post(reverse('messaging:compose'), {
            'subject': 'My Draft',
            'body': 'Draft content',
            'action': 'draft',
        })
        self.assertEqual(response.status_code, 302)
        msg = Message.objects.get(subject='My Draft')
        self.assertEqual(msg.status, 'draft')

    def test_send_without_recipient_shows_error(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.post(reverse('messaging:compose'), {
            'subject': 'No Recipient',
            'body': 'body',
            'action': 'send',
        })
        # Should re-render the form, not redirect
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'recipient')

    # ── View message tests ───────────────────────────────────────────────────

    def test_recipient_can_view_message(self):
        msg = Message.objects.create(
            sender=self.user2, recipient=self.user1,
            subject='View me', body='content', status='sent'
        )
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('messaging:view_message', args=[msg.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View me')

    def test_viewing_message_marks_it_as_read(self):
        msg = Message.objects.create(
            sender=self.user2, recipient=self.user1,
            subject='Mark read', body='content', status='sent'
        )
        self.assertFalse(msg.is_read)
        self.client.login(username='alice', password='pass1234')
        self.client.get(reverse('messaging:view_message', args=[msg.pk]))
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)

    def test_third_party_cannot_view_message(self):
        """A user who is neither sender nor recipient gets 404."""
        user3 = User.objects.create_user('charlie', 'c@test.com', 'pass1234')
        msg = Message.objects.create(
            sender=self.user1, recipient=self.user2,
            subject='Private', body='secret', status='sent'
        )
        self.client.login(username='charlie', password='pass1234')
        response = self.client.get(reverse('messaging:view_message', args=[msg.pk]))
        self.assertEqual(response.status_code, 404)

    # ── Delete tests ─────────────────────────────────────────────────────────

    def test_recipient_can_delete_from_inbox(self):
        msg = Message.objects.create(
            sender=self.user2, recipient=self.user1,
            subject='Delete me', body='body', status='sent'
        )
        self.client.login(username='alice', password='pass1234')
        self.client.post(reverse('messaging:delete_message', args=[msg.pk]))
        msg.refresh_from_db()
        self.assertTrue(msg.deleted_by_recipient)

    def test_sender_can_delete_from_sent(self):
        msg = Message.objects.create(
            sender=self.user1, recipient=self.user2,
            subject='Delete sent', body='body', status='sent'
        )
        self.client.login(username='alice', password='pass1234')
        self.client.post(reverse('messaging:delete_message', args=[msg.pk]))
        msg.refresh_from_db()
        self.assertTrue(msg.deleted_by_sender)
