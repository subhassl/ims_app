from django.urls import path
from .views import CreateSaleView, SaleView, ItemCategoryReportByDate, CustomerReportByDate

urlpatterns = [
    path('create-sale/', CreateSaleView.as_view()),
    path('sale-details/', SaleView.as_view()),
   
    path('itemCategory-report/', ItemCategoryReportByDate.as_view()),
    path('cust-report/', CustomerReportByDate.as_view(),)
]
