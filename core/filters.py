from django import forms
from django.db import models
from django_filters import FilterSet
import django_filters

from .models import Ticket, Task, Product


class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'name': ['icontains'],
            'state': ['exact']
        }


class TaskFilter(FilterSet):
    task_description = django_filters.CharFilter(field_name='task_description', lookup_expr='icontains',
                                                 widget=forms.TextInput(attrs={'class': 'uk-input'}))
    state = django_filters.ChoiceFilter(field_name='state', choices=Task.STATE,
                                        widget=forms.Select(attrs={'class': 'uk-select'}))

    class Meta:
        model = Task
        fields = ('task_description', 'state')


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains']
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'widget': forms.TextInput(attrs={'class': 'uk-input'}),
                },
            },
        }
