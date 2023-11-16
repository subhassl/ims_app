
from .models import ItemStock
from rest_framework.views import APIView
from rest_framework.response import Response
from master.views import AuthRequiredApiView

class GetStockDetails(AuthRequiredApiView):

    def get(self, request):
        stock_id = request.GET.get("stock_id")
        stock = ItemStock.objects.get(id=stock_id)
        stock_details = ItemStock.objects.filter(id=stock_id).values('item__name', 'stock')
        return Response(stock_details)


class ListStockDetails(AuthRequiredApiView):

    def get(self, request):
        stock_list = ItemStock.objects.all().values('id', 'item__name', 'stock')
        return Response(stock_list)


