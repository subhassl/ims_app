from django.urls import path
from .views import CreateSaleView, GetSingleSale, Listsale, ItemCategoryReportByDate, CustomerReportByDate

urlpatterns = [
    path('create-sale/', CreateSaleView.as_view()),
    path('get-single-sale/', GetSingleSale.as_view()),
    path('list-sale/', Listsale.as_view()),
    path('itemCategory-report/', ItemCategoryReportByDate.as_view()),
    path('cust-report/', CustomerReportByDate.as_view(),)
]
