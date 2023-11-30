from django.urls import path
from .views import InteractorView, ItemCategoryView, ItemView, CreateInteractor, CreateItem, UpdateItem, UpdateInteractor,  CreateItemCategory, GetItemView


urlpatterns = [
    
    path('interactors/', InteractorView.as_view(), name='interactor-list'),
    path('create-interactor/',CreateInteractor.as_view()),
    path('update-interactor/', UpdateInteractor.as_view()),
    path('create-item-category/', CreateItemCategory.as_view()),
    path('item-categories/', ItemCategoryView.as_view(), name='item-category-list'),
    path('create-item/', CreateItem.as_view()),

    
    path('items/', ItemView.as_view(), name='item-list'),
    path('get-item/', GetItemView.as_view()),
    path('update-item/', UpdateItem.as_view()),
]
