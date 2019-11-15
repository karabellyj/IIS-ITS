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


class TicketCreateView(CreateView):
    model = Ticket
    fields = ('name', 'description', 'product', 'author',)
    success_url = reverse_lazy('core:ticket-list')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['author'] = self.request.user.pk
        return initial


class TicketDetailView(DetailView):
    model = Ticket


class TicketUpdateView(UpdateView):
    model = Ticket
    fields = ('name', 'description', 'product')
    success_url = reverse_lazy('core:ticket-list')


class ProductListView(FilterView):
    model = Product
    paginate_by = 25
    filterset_fields = ('name',)
    template_name = 'core/product_list.html'


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'manager', 'parent',)
    success_url = reverse_lazy('core:product-list')


class ProductDetailView(DetailView):
    model = Product


class TaskListView(FilterView):
    model = Task
    filterset_fields = ('state',)
    template_name = 'core/task_list.html'


class TaskCreateView(CreateView):
    model = Task
    fields = ('description', 'state', 'estimated', 'employee',)
    success_url = reverse_lazy('core:task-list')


class TaskDetailView(DetailView):
    model = Task


class CommentCreateView(CreateView):
    model = Comment
    fields = ('text', 'ticket', 'user')
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['ticket'] = self.kwargs.get(self.pk_url_kwarg)
        initial['user'] = self.request.user.pk
        return initial


class AttachmentCreateView(CreateView):
    model = Attachment
    fields = ('name', 'file', 'ticket',)
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['ticket'] = self.request.GET.get('ticket')
        return initial
