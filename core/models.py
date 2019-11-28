from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from model_utils import Choices
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from users.models import Employee, Manager


class Comment(models.Model):
    text = models.TextField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comments')


class Ticket(models.Model):
    STATE = Choices(('analysis', _('analysis')), ('resolving', _('resolving')), ('implementing', _('implementing')),
                    ('testing', _('testing')), ('done', _('done')))
    name = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(max_length=255, choices=STATE, default=STATE.analysis)
    created = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='tickets')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        permissions = [
            ('change_state_ticket', 'Can change the state of tickets'),
        ]

    def __str__(self):
        return self.name


class Attachment(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()

    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='attachments')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATE = Choices(('analysis', _('analysis')), ('resolving', _('resolving')), ('implementing', _('implementing')),
                    ('testing', _('testing')), ('done', _('done')))
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=STATE, default=STATE.analysis)
    estimated = models.DurationField()
    reported = models.DurationField(null=True, blank=True)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.description


class Product(MPTTModel):
    name = models.CharField(max_length=255, unique=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='products')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
