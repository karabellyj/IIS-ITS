from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

from core import models
from users.models import User

GROUPS_PERMISSIONS = {
    'Customers': {
        models.Ticket: ['add', 'change', 'delete', 'view'],
        models.Comment: ['add', 'change', 'view'],
        models.Attachment: ['add', 'view', 'delete'],
    },
    'Employees': {
        # Customers permissions
        models.Ticket: ['add', 'change', 'delete', 'view'],
        models.Comment: ['add', 'change', 'view'],
        models.Attachment: ['add', 'view', 'delete'],

        # Employees permissions
        models.Task: ['change', 'view']
    },
    'Managers': {
        # Customers permissions
        models.Ticket: ['add', 'change', 'delete', 'view', 'change_ticket_state'],
        models.Comment: ['add', 'change', 'view'],
        models.Attachment: ['add', 'view', 'delete'],

        # Employees permissions + Manager permissions
        models.Task: ['add', 'change', 'view', 'delete'],
        models.Product: ['view']
    },
    'Leads': {
        # Customers permissions
        models.Ticket: ['add', 'change', 'delete', 'view'],
        models.Comment: ['add', 'change', 'view'],
        models.Attachment: ['add', 'view', 'delete'],

        # Employees permissions + Manager permissions
        models.Task: ['add', 'change', 'view', 'delete'],

        # Lead permissions
        models.Product: ['add', 'change', 'view', 'delete']
    },
    'Admins': {
        # Customers permissions
        models.Ticket: ['add', 'change', 'delete', 'view'],
        models.Comment: ['add', 'change', 'view'],
        models.Attachment: ['add', 'view', 'delete'],

        # Employees permissions + Manager permissions
        models.Task: ['add', 'change', 'view', 'delete'],

        # Lead permissions
        models.Product: ['add', 'change', 'view', 'delete'],

        # Admin permissions
        User: ['add', 'change', 'view', 'delete']
    }
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        # Loop groups
        for group_name in GROUPS_PERMISSIONS:

            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for model_cls in GROUPS_PERMISSIONS[group_name]:

                # Loop permissions in group/model
                for perm_index, perm_name in enumerate(GROUPS_PERMISSIONS[group_name][model_cls]):

                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write("Adding "
                                          + codename
                                          + " to group "
                                          + group.__str__())
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
