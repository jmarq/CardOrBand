from django.db import models

# Create your models here.


class Card(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name
