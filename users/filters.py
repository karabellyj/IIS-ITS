from django import forms
from django.db import models
from django_filters import FilterSet
import django_filters

from .models import User


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'email': ['icontains']
        }
        filter_overrides = {
            models.EmailField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'widget': forms.TextInput(attrs={'class': 'uk-input'}),
                },
            },
        }
