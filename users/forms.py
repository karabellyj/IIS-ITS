from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db import transaction

from .utils import get_user_class_by_type, get_user_group_by_type
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
        group = Group.objects.get(name='Customers')
        user.groups.add(group)

        return user


class AllUsersCreateForm(UserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        model = User
        fields = CustomUserCreationForm.Meta.fields + ('first_name', 'last_name', 'user_type')

    @transaction.atomic
    def save(self):
        user = super().save()

        user_cls = get_user_class_by_type(user.user_type)
        user_cls.objects.create(user=user)

        user_group = get_user_group_by_type(user.user_type)
        group = Group.objects.get(name=user_group)
        user.groups.add(group)

        return user
