from django.http import Http404

from users.models import Customer, Employee, Manager, Lead, Admin


def get_user_class_by_type(user_type):
    type_to_cls = {0: Customer, 1: Employee, 2: Manager, 3: Lead, 4: Admin}
    try:
        cls = type_to_cls[user_type]
    except KeyError:
        raise Http404

    return cls


def get_user_group_by_type(user_type):
    type_to_group = {0: 'Customers', 1: 'Employees', 2: 'Managers', 3: 'Leads', 4: 'Admins'}
    try:
        cls = type_to_group[user_type]
    except KeyError:
        raise Http404

    return cls
