from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils.translation import gettext as _

from .models import User, Customer
from .utils import get_user_class_by_type, get_user_group_by_type


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomerSignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'uk-input', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'uk-input', 'placeholder': 'Password confirmation'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(CustomUserCreationForm.Meta):
        model = User
        fields = CustomUserCreationForm.Meta.fields + ('first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'uk-input', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'uk-input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'uk-input', 'placeholder': 'Last name'})
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = self.Meta.model.USER_TYPES.customer
        user.save()

        customer = Customer.objects.create(user=user)
        group = Group.objects.get(name='Customers')
        user.groups.add(group)

        return user


class AllUsersCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'uk-input'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'uk-input'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(CustomUserCreationForm.Meta):
        model = User
        fields = CustomUserCreationForm.Meta.fields + ('first_name', 'last_name', 'user_type')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'uk-input'}),
            'first_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'last_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'user_type': forms.Select(attrs={'class': 'uk-select'})
        }

    @transaction.atomic
    def save(self):
        user = super().save()

        user_cls = get_user_class_by_type(user.user_type)
        user_cls.objects.create(user=user)

        user_group = get_user_group_by_type(user.user_type)
        group = Group.objects.get(name=user_group)
        user.groups.add(group)

        return user
