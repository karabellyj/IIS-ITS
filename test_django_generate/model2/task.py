#-*- coding: utf-8 -*-

from django.db import models

class Task(models.Model):
    class Meta:
        pass

    description = undefined(max_length=255)
    state = undefined()
    estimated = undefined()
    reported = undefined()

     = models.ForeignKey('Employee', on_delete=models.PROTECT)

