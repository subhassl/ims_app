from django.urls import path
from .views import GetStockDetails, ListStockDetails

urlpatterns = [
    path('get-stock-details/', GetStockDetails.as_view()),
    path('list-stock-details/', ListStockDetails.as_view()),
]
