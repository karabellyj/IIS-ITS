from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from .models import User, Customer


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomerSignUpForm(UserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = self.Meta.model.USER_TYPES.customer
        user.save()
        customer = Customer.objects.create(user=user)
        return user


class AllUsersCreateForm(UserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        model = User
        fields = CustomUserCreationForm.Meta.fields + ('first_name', 'last_name', 'user_type')
