#-*- coding: utf-8 -*-

from django.db import models

class Commnet(models.Model):
    class Meta:
        pass

    text = undefined()

     = models.ForeignKey('User', on_delete=models.PROTECT)

