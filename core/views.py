from datetime import datetime, timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django_filters.views import FilterView

from users.models import User
from .filters import TicketFilter, TaskFilter, ProductFilter
from .forms import CommentForm, AttachmentForm, AddTicketForm, AddProductForm, AddTaskForm, UpdateTaskForm, \
    UpdateStateTicketForm
from .models import Ticket, Product, Task


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.select_related('author').all()
        context['STATES'] = Ticket.STATE
        return context


class MyTicketListView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.select_related('author').filter(author=self.request.user).all()
        context['STATES'] = Ticket.STATE
        return context


class DashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'dashboard.html'

    def test_func(self):
        return True if self.request.user.is_authenticated and self.request.user.user_type > 0 else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        one_week_ago = datetime.today() - timedelta(days=7)
        context['USER_TYPES'] = User.USER_TYPES

        if self.request.user.user_type == User.USER_TYPES.employee:
            context['number_of_unfinished_tasks'] = Task.objects.filter(employee__user=self.request.user).exclude(
                state=Task.STATE.done).count()
            context['your_tasks'] = Task.objects.filter(employee__user=self.request.user).all()
        if self.request.user.user_type == User.USER_TYPES.manager:
            context['number_of_assigned_unfinished_tasks'] = Task.objects.filter(created_by=self.request.user).exclude(
                state=Task.STATE.done).count()
            context['number_of_unresolved_tickets'] = Ticket.objects.filter(
                product__manager__user=self.request.user).exclude(
                state__in=[Ticket.STATE.rejected, Ticket.STATE.done]
            ).count()
            context['your_tasks'] = Task.objects.filter(created_by=self.request.user).all()
            context['your_tickets'] = Ticket.objects.filter(product__manager__user=self.request.user).all()
        if self.request.user.user_type == User.USER_TYPES.lead or self.request.user.user_type == User.USER_TYPES.admin:
            context['number_of_new_tickets_this_week'] = Ticket.objects.filter(created__gte=one_week_ago).count()
        if self.request.user.user_type == User.USER_TYPES.admin:
            context['number_of_new_customers_this_week'] = User.objects.filter(user_type=User.USER_TYPES.customer,
                                                                               date_joined__gte=one_week_ago).count()
        return context


class TicketListView(FilterView):
    model = Ticket
    filterset_class = TicketFilter
    paginate_by = 25
    template_name = 'core/ticket_list.html'


class TicketCreateView(PermissionRequiredMixin, CreateView):
    form_class = AddTicketForm
    template_name = 'core/ticket_form.html'
    success_url = reverse_lazy('home')
    permission_required = ('core.add_ticket',)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['author'] = self.request.user.pk
        return initial


class TicketDetailView(DetailView):
    model = Ticket


class TicketUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ('name', 'description', 'product')
    success_url = reverse_lazy('home')
    permission_required = ('core.change_ticket',)
    template_name = 'core/ticket_update_form.html'

    def test_func(self):
        return True if self.request.user == self.get_object().author else False


class TicketStateUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    form_class = UpdateStateTicketForm
    template_name = 'core/ticket_form.html'
    success_url = reverse_lazy('home')
    permission_required = ('core.change_state_ticket',)

    def test_func(self):
        return True if self.request.user == self.get_object().product.manager.user else False


class ProductListView(PermissionRequiredMixin, FilterView):
    model = Product
    paginate_by = 25
    filterset_class = ProductFilter
    template_name = 'core/product_list.html'
    permission_required = ('core.view_product',)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    form_class = AddProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('core:product-list')
    permission_required = ('core.add_product',)


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('core:product-list')
    permission_required = ('core.change_product',)


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('core:product-list')
    permission_required = ('core.delete_product',)


class ProductDetailView(PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = ('core.view_product',)


class TaskListView(PermissionRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'core/task_list.html'
    permission_required = ('core.view_task',)


class TaskCreateView(PermissionRequiredMixin, CreateView):
    form_class = AddTaskForm
    template_name = 'core/task_form.html'
    success_url = reverse_lazy('core:task-list')
    permission_required = ('core.add_task',)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['created_by'] = self.request.user.pk
        return initial


class TaskDetailView(PermissionRequiredMixin, DetailView):
    model = Task
    permission_required = ('core.view_task',)



class TaskUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = 'core/task_form.html'
    success_url = reverse_lazy('core:task-list')
    permission_required = ('core.change_task',)

    def test_func(self):
        return True if self.request.user == self.get_object().employee.user or self.request.user == self.get_object().created_by else False


class TaskDeleteView(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('core:task-list')
    permission_required = ('core.delete_task',)

    def test_func(self):
        return True if self.request.user == self.get_object().created_by else False


class CommentCreateView(PermissionRequiredMixin, CreateView):
    form_class = CommentForm
    success_url = reverse_lazy('home')
    template_name = 'core/comment_form.html'
    permission_required = ('core.add_comment',)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['ticket'] = self.kwargs.get(self.pk_url_kwarg)
        self.success_url = reverse('core:ticket-detail', kwargs={'pk': initial['ticket']})
        initial['user'] = self.request.user.pk
        return initial


class AttachmentCreateView(PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AttachmentForm
    template_name = 'core/attachment_form.html'
    success_url = reverse_lazy('home')
    permission_required = ('core.add_attachment',)

    def test_func(self):
        task = get_object_or_404(Ticket, pk=self.kwargs.get(self.pk_url_kwarg))
        return True if self.request.user == task.author else False

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['ticket'] = self.kwargs.get(self.pk_url_kwarg)
        return initial
