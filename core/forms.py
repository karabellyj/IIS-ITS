from django import forms

from .models import Comment, Attachment


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
