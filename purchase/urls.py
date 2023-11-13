from django.urls import path
from .views import PurchaseView, PurchaseListView, RetrivePurchaseData

urlpatterns = [
    path('create-purchase/', PurchaseView.as_view()),
    path('list-purchase/', PurchaseListView.as_view()),
    path('get-purchase-details/',RetrivePurchaseData.as_view())
]
