from django.db import models
from django.contrib.auth.models import User

class Dish(models.Model):
    name = models.CharField(max_length=100, help_text="Name of dish")
    description = models.CharField(max_length=300)
    price = models.FloatField(default=0)
    order = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
