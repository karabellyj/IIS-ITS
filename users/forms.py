from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db import transaction

from .models import User, Customer, Employee, Manager, Lead


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

        user_type_to_cls = {0: Customer, 1: Employee, 2: Manager, 3: Lead, }  # TODO: add
        user_type_to_group = {0: 'Customers', 1: 'Employees'}  # TODO: add all groups
        user_cls = user_type_to_cls[user.user_type]
        user_cls.objects.create(user=user)

        user_group = user_type_to_group[user.user_type]
        group = Group.objects.get(name=user_group)
        user.groups.add(group)

        return user
