from django import forms

from .models import Comment, Attachment, Ticket, Product, Task


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


class UpdateStateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('state',)
        widgets = {
            'state': forms.Select(attrs={'class': 'uk-select'})
        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'manager', 'parent',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'uk-input'}),
            'manager': forms.Select(attrs={'class': 'uk-select'}),
            'parent': forms.Select(attrs={'class': 'uk-select'}),
        }


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_description', 'state', 'estimated', 'employee', 'created_by',)
        widgets = {
            'task_description': forms.TextInput(attrs={'class': 'uk-input'}),
            'state': forms.Select(attrs={'class': 'uk-select'}),
            'estimated': forms.TimeInput(attrs={'class': 'uk-input', 'placeholder': 'hh:mm:ss'}),
            'employee': forms.Select(attrs={'class': 'uk-select'}),
            'created_by': forms.HiddenInput
        }


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('solution_description', 'state', 'reported',)
        widgets = {
            'solution_description': forms.TextInput(attrs={'class': 'uk-input'}),
            'state': forms.Select(attrs={'class': 'uk-select'}),
            'reported': forms.TimeInput(attrs={'class': 'uk-input', 'placeholder': 'hh:mm:ss'}),
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
