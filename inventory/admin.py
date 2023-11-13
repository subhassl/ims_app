from django.contrib import admin
from .models import ItemStock

# Register your models here.
@admin.register(ItemStock)
class ItemStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'stock',)   
    search_fields = ('id', 'iteam')