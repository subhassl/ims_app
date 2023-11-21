from django.urls import path
from .views import CreateSaleView, GetSingleSale, Listsale

urlpatterns = [
    path('create-sale/', CreateSaleView.as_view()),
    path('get-single-sale/', GetSingleSale.as_view()),
    path('list-sale/', Listsale.as_view()),
]
