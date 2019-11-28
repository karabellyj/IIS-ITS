from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .utils import get_user_group_by_type, get_user_class_by_type
from .filters import UserFilter
from .models import User
from .forms import CustomerSignUpForm, AllUsersCreateForm


class SignUpView(CreateView):
    form_class = CustomerSignUpForm
    success_url = reverse_lazy('home')
    template_name = 'users/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = User.USER_TYPES.customer
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class UserListView(PermissionRequiredMixin, FilterView):
    model = User
    paginate_by = 25
    filterset_class = UserFilter
    permission_required = ('users.view_user',)
    template_name = 'users/user_list.html'


class UserDetailView(PermissionRequiredMixin, DetailView):
    model = User
    context_object_name = 'user_object'
    permission_required = ('users.view_user',)


class UserCreateView(PermissionRequiredMixin, CreateView):
    form_class = AllUsersCreateForm
    success_url = reverse_lazy('users:user-list')
    permission_required = ('users.add_user',)
    template_name = 'users/user_form.html'

    def form_valid(self, form):
        user = form.save()
        return redirect(self.success_url)


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    fields = ('email', 'first_name', 'last_name', 'user_type')
    success_url = reverse_lazy('users:user-list')
    permission_required = ('users.change_user',)

    @transaction.atomic
    def form_valid(self, form):
        if 'user_type' in form.changed_data:
            self.object.groups.clear()
            group = Group.objects.get(name=get_user_group_by_type(self.object.user_type))
            self.object.groups.add(group)

            user_cls = get_user_class_by_type(self.object.user_type)
            user_cls.objects.get(user=self.object).delete()

            new_user_cls = get_user_class_by_type(form.cleaned_data['user_type'])
            new_user_cls.objects.create(user=self.object)

        form.save()

        return redirect(self.success_url)


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:user-list')
    context_object_name = 'user_object'
    permission_required = ('users.delete_user',)
