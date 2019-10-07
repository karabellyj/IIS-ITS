from django.db import models

# Create your models here.

class Comment(models.Model):
    text = models.TextField()


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    created = models.DateTimeField()


class Attachment(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField()

class Task(models.Model):
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    estimated = models.DateTimeField()
    reported = models.DateTimeField()


class Product(models.Model):
    pass