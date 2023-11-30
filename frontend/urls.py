from django.urls import path
from .views import interactor_list, create_interactor

urlpatterns = [
    path('list-interactors/', interactor_list,),
    path('create-interactor/', create_interactor),    
]
