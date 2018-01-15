from django.db import models

# Create your models here.


class Card(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    correct = models.IntegerField(null=False, blank=False, default=0)
    incorrect = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.name

    def add_correct(self):
        self.correct += 1
        self.save()

    def add_incorrect(self):
        self.incorrect += 1
        self.save()


class Band(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    correct = models.IntegerField(null=False, blank=False, default=0)
    incorrect = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.name

    def add_correct(self):
        self.correct += 1
        self.save()

    def add_incorrect(self):
        self.incorrect += 1
        self.save()
