from django import forms
from django.contrib.auth.models import User
from .models import Message


class ComposeMessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        help_text="Leave empty to save as draft."
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'})
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Write your message here...'
        })
    )

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if current_user:
            # Exclude the logged-in user from recipient list
            self.fields['recipient'].queryset = User.objects.exclude(pk=current_user.pk).order_by('username')

    def clean(self):
        cleaned = super().clean()
        # If trying to send (not draft), recipient is required
        # The view will pass action='send' or 'draft' — handled in view
        return cleaned
