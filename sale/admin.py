from django.contrib import admin
from .models import Sale, SaleLine

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'interactor', 'created_at','created_by', 'total_quantity',)
    list_filter =  ('interactor',)
    search_fields = ('interactor', 'created_by')

@admin.register(SaleLine)
class SaleLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'item','quantity', 'rate', 'amount',)
    search_fields = ('item', 'Sale ')

