from django.db import models


class TimeStampedModel(models.Model):

    created = models.DateField(auto_now_add=True)

    edited = models.DateField(auto_now=True)

    class Meta:
        abstract = True
