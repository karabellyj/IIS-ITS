from django import forms

from .models import Comment, Attachment, Ticket


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('name', 'description', 'product', 'author',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'uk-input'}),
            'description': forms.Textarea(attrs={'class': 'uk-textarea'}),
            'product': forms.Select(attrs={'class': 'uk-select'}),
            'author': forms.HiddenInput,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'ticket', 'user')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'uk-textarea'}),
            'ticket': forms.HiddenInput,
            'user': forms.HiddenInput
        }


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('name', 'image', 'ticket',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'uk-input'}),
            'ticket': forms.HiddenInput,
        }
