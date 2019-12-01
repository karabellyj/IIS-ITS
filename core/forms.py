from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'ticket', 'user')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'uk-textarea'}),
            'ticket': forms.HiddenInput,
            'user': forms.HiddenInput
        }
