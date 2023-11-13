from django.urls import path
from .views import PurchaseView

urlpatterns = [
    path('create-purchase/', PurchaseView.as_view())
]
