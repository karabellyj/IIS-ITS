from django_filters import FilterSet

from .models import Ticket, Task, Product


class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'name': ['icontains'],
            'state': ['exact']
        }


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = {
            'task_description': ['icontains'],
            'state': ['exact']
        }


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains']
        }
