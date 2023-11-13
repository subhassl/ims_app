from django.contrib import admin
from .models import Purchase, PurchaseLine


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('interactor', 'created_at','total_quantity', 'total_amount')
    list_filter =  ('interactor', 'created_at', 'created_by',)
    search_fields = ('intractor', 'created_at')


@admin.register(PurchaseLine)
class PurchaseLineAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'item','quantity', 'rate')
    list_filter =  ('item',)
    search_fields = ('purchase', 'item')