from django.urls import path
from .views import InteractorView, ItemCategoryView

urlpatterns = [
    path('interactors/', InteractorView.as_view(), name='interactor-list'),
    path('item-categories/', ItemCategoryView.as_view(), name='item-category-list'),
]
