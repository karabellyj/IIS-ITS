from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TicketFilter
from .models import Ticket, Product, Task, Comment, Attachment


class TicketListView(FilterView):
    model = Ticket
    filterset_class = TicketFilter
    paginate_by = 25
    template_name = 'core/ticket_list.html'


class TicketCreateView(PermissionRequiredMixin, CreateView):
    model = Ticket
    fields = ('name', 'description', 'product', 'author',)
    success_url = reverse_lazy('core:ticket-list')
    permission_required = ('core.add_ticket',)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['author'] = self.request.user.pk
        return initial


class TicketDetailView(DetailView):
    model = Ticket


class TicketUpdateView(PermissionRequiredMixin, UpdateView):
    model = Ticket
    fields = ('name', 'description', 'product')
    success_url = reverse_lazy('core:ticket-list')
    permission_required = ('core.change_ticket',)  # TODO: only owner should be able to change


class ProductListView(PermissionRequiredMixin, FilterView):
    model = Product
    paginate_by = 25
    filterset_fields = ('name',)
    template_name = 'core/product_list.html'
    permission_required = ('core.view_product',)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'manager', 'parent',)
    success_url = reverse_lazy('core:product-list')
    permission_required = ('core.add_product',)


class ProductDetailView(PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = ('core.view_product',)


class TaskListView(PermissionRequiredMixin, FilterView):
    model = Task
    filterset_fields = ('state',)
    template_name = 'core/task_list.html'
    permission_required = ('core.view_task',)


class TaskCreateView(PermissionRequiredMixin, CreateView):
    model = Task
    fields = ('description', 'state', 'estimated', 'employee',)
    success_url = reverse_lazy('core:task-list')
    permission_required = ('core.add_task',)


class TaskDetailView(PermissionRequiredMixin, DetailView):
    model = Task
    permission_required = ('core.view_task',)


class CommentCreateView(PermissionRequiredMixin, CreateView):
    model = Comment
    fields = ('text', 'ticket', 'user')
    success_url = reverse_lazy('home')
    permission_required = ('core.add_comment',)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['ticket'] = self.kwargs.get(self.pk_url_kwarg)
        initial['user'] = self.request.user.pk
        return initial


class AttachmentCreateView(PermissionRequiredMixin, CreateView):
    model = Attachment
    fields = ('name', 'image', 'ticket',)
    success_url = reverse_lazy('home')
    permission_required = ('core.add_attachment',)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['ticket'] = self.kwargs.get(self.pk_url_kwarg)
        return initial
