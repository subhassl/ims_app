from django.urls import path
from .views import PurchaseView

urlpatterns = [
    path('purchases/', PurchaseView.as_view())
]
