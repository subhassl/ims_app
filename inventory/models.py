from django.db import models
from master.models import Item

# Create your models here.
class ItemStock(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits=10, default=0, decimal_places=2)

    def __str__(self):
        return self.item.name
    


    

    
