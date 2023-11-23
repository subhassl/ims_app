from django.urls import path
from .views import PurchaseView, PurchaseListView, RetrivePurchaseData, FetchPurchaseDataBasedOnDate

urlpatterns = [
    path('create-purchase/', PurchaseView.as_view()),
    path('list-purchase/', PurchaseListView.as_view()),
    path('get-purchase-details/',RetrivePurchaseData.as_view()),
    path('date-based-report/', FetchPurchaseDataBasedOnDate.as_view()),
]
