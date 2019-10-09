from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from users.models import Employee


class Comment(models.Model):
    text = models.TextField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comments')


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    created = models.DateTimeField()

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='tickets')


class Attachment(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField()

    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='attachments')


class Task(models.Model):
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    estimated = models.DateTimeField()
    reported = models.DateTimeField()

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')


class Product(MPTTModel):
    name = models.CharField(max_length=255, unique=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
