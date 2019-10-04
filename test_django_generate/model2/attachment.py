#-*- coding: utf-8 -*-

from django.db import models

class Attachment(models.Model):
    class Meta:
        pass

    name = undefined()
    file = undefined()

     = models.ForeignKey('Ticket', on_delete=models.PROTECT)

