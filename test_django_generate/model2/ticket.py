#-*- coding: utf-8 -*-

from django.db import models

class Ticket(models.Model):
    class Meta:
        pass

    name = undefined(max_length=255)
    description = undefined(max_length=255)
    state = undefined()
    created = undefined()

     = models.ForeignKey('User', on_delete=models.PROTECT)
     = models.ForeignKey('Product', on_delete=models.PROTECT)

