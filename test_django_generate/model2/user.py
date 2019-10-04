#-*- coding: utf-8 -*-

from django.db import models

class User(models.Model):
    class Meta:
        pass

    name = undefined(max_length=255)
    surname = undefined(max_length=255)
    email = undefined()
    password = undefined()


