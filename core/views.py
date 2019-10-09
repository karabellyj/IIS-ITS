from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_filters.views import FilterView

from .filters import TicketFilter
from .models import Ticket, Product


class TicketListView(FilterView):
    model = Ticket
    filterset_class = TicketFilter
    paginate_by = 25
    template_name = 'core/ticket_list.html'


class TicketCreateView(CreateView):
    model = Ticket
    fields = ('name', 'description', 'product',)
    success_url = reverse_lazy('core:ticket-list')


class ProductListView(FilterView):
    model = Product
    paginate_by = 25
    filterset_fields = ('name',)
    template_name = 'core/product_list.html'


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'parent',)
    success_url = reverse_lazy('core:product-list')
