#-*- coding: utf-8 -*-

from django.db import models

class Product(models.Model):
    class Meta:
        pass

    manager = models.ForeignKey('Manager', on_delete=models.PROTECT)

