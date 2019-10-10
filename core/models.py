from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from users.models import Employee, Manager


class Comment(models.Model):
    text = models.TextField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comments')


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='tickets')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')


class Attachment(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField()

    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='attachments')


class Task(models.Model):
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    estimated = models.DurationField()
    reported = models.DurationField(null=True, blank=True)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')


class Product(MPTTModel):
    name = models.CharField(max_length=255, unique=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='products')

    class MPTTMeta:
        order_insertion_by = ['name']
