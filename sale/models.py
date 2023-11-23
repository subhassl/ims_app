from django.db import models
from master.models import Interactor, Item
from django.contrib.auth.models import User
from agent.models import Agent

class Sale(models.Model):
    interactor = models.ForeignKey(Interactor, on_delete=models.PROTECT, related_name='interactor_sales')
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, related_name='agent')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT )
    total_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class SaleLine(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.CASCADE )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # def __str__(self):
    #     return self.name


 
