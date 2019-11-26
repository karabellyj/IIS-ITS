from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .filters import UserFilter
from .models import User, Lead, Manager, Employee, Customer
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


class UserUpdateView(PermissionRequiredMixin, CreateView):
    model = User
    fields = ('first_name', 'last_name', 'user_type')
    success_url = reverse_lazy('users:user-list')
    permission_required = ('users.change_user',)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()

        for field in self.fields:
            initial[field] = getattr(self.get_object(), field)
        return initial

    def form_valid(self, form):
        print('here')
        if 'user_type' in form.changed_data:
            user_type_to_cls = {0: Customer, 1: Employee, 2: Manager, 3: Lead, }  # TODO: add
            user_type_to_group = {0: 'Customers', 1: 'Employees'}  # TODO: add all groups

            self.get_object().groups.clear()
            group = Group.objects.get(name=user_type_to_group[self.get_object().user_type])
            self.get_object().groups.add(group)

            user_cls = user_type_to_cls[self.get_object().user_type]
            user_cls.objects.get(user=self.get_object()).delete()

            new_user_cls = user_type_to_cls[form.cleaned_data['user_type']]
            new_user_cls.objects.create(user=self.get_object())

        user = User.objects.get(pk=self.get_object().id)
        user.save(update_fields=form.changed_data)

        return redirect(self.success_url)


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:user-list')
    context_object_name = 'user_object'
    permission_required = ('users.delete_user',)
