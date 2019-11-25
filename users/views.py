from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView

from .filters import UserFilter
from .models import User, Employee, Customer, Manager, Lead
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
        user_type_to_cls = {0: Customer, 1: Employee, 2: Manager, 3: Lead, }  # TODO: add admin
        user = form.save()

        user_cls = user_type_to_cls[user.user_type]
        user_cls.objects.create(user=user)

        return redirect(self.success_url)
