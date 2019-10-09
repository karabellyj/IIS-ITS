from django_filters.views import FilterView

from .filters import TicketFilter
from .models import Ticket


class TicketListView(FilterView):
    model = Ticket
    filterset_class = TicketFilter
    paginate_by = 25
    template_name = 'core/ticket_list.html'