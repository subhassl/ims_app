from django.urls import path
from .views import interactor_list, create_interactor, list_itemCategory, list_sale

urlpatterns = [
    path('list-interactors/', interactor_list,),
    path('create-interactor/', create_interactor),
    path('list-item-category/', list_itemCategory),
    path('list-sale/', list_sale),  

]
