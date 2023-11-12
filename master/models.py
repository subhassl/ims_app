from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Interactor(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


class ItemCategory(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=20)
    item_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)




