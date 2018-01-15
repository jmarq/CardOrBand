from django.db import models

# Create your models here.


class Question(models.Model):
    # base model for Card and Band models
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


class Card(Question):
    pass


class Band(Question):
    pass
