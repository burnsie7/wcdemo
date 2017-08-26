from __future__ import unicode_literals

import datetime


from django.db import models


class Maker(models.Model):

    def __str__(self):
        return ' - '.join([str(self.id), self.name, self.description])

    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)


class Widget(models.Model):

    class Meta:
        unique_together = (('name', 'cost'))

    def __str__(self):
        return ' - '.join([str(self.id), self.name, str(self.cost), self.description])

    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    cost = models.DecimalField(max_digits=100, decimal_places=2)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    created_date = models.DateField(default=datetime.date.today)


class Order(models.Model):

    class Meta:
        unique_together = (('name', 'order_date'))

    def __str__(self):
        return ' - '.join([str(self.id), self.name])

    name = models.CharField(max_length=1024)
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)
    order_date = models.DateField(default=datetime.date.today)

    def random_index(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return random_index
