from django import forms
from django.contrib.auth import get_user_model          # ← CORRECT
from .models import Message

User = get_user_model()                                 # ← add this line


class ComposeMessageForm(forms.ModelForm):

    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label="Select Recipient",
        widget=forms.Select(
            attrs={
                'class': 'form-select form-control'
            }
        ),
        help_text="Leave empty to save as draft."
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
            }
        )
    )

    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Write your message here...'
            }
        )
    )

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if current_user:
            self.fields['recipient'].queryset = (
                User.objects
                .exclude(pk=current_user.pk)
                .order_by('username')
            )