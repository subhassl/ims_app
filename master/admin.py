from django.contrib import admin
from .models import Interactor, ItemCategory, Item


@admin.register(Interactor)
class IntercatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number','address')
    list_filter =  ('is_active',)
    search_fields = ('name', 'phone_number')


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_code', 'is_active', 'category')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'item_code')

    