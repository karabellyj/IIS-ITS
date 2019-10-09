from django_filters import FilterSet

from .models import Ticket


class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = ('name', 'state')
