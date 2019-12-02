from django_filters import FilterSet

from .models import User


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'email': ['icontains']
        }
