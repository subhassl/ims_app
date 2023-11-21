from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from master.views import AuthRequiredApiView
from inventory.models import ItemStock 
from .models import Sale, SaleLine



# create Sale
class CreateSaleView(AuthRequiredApiView):

    def post(self, request):
        sale_data = request.data
        sale = Sale.objects.create(
            interactor_id=sale_data["interactor_id"],
            created_by=request.user
        )

        # loop through lines array received in request data and create sale line
        for line in sale_data["lines"]:
            item_id = line["item_id"]
            quantity = line['quantity']
            rate = line['rate']
            amount = quantity * rate

            # creating sale line in SaleLine table
            SaleLine.objects.create(
                sale_id=sale.id,
                item_id=item_id,
                quantity=quantity,
                rate=rate,
                amount=amount
            )


            item_stock, x = ItemStock.objects.get_or_create(item_id=item_id)
            if quantity > item_stock.stock:
                pass
            item_stock.stock -= quantity
            item_stock.save()

            # update total quantity and total amount in sale object
            sale.total_quantity += quantity
            sale.total_amount += amount

        sale.save()

        return Response({
            "id": sale.id
        })

# Get single Sale data

class GetSingleSale(AuthRequiredApiView):
    def get(self, request):
        sale_id = request.GET.get('sale_id')
        sale = Sale.objects.get(id=sale_id)
        sale_line = SaleLine.objects.filter(sale_id=sale_id).values('item_id', 'item__name', 'quantity', 'rate', 'amount',)
        sale_dict = {
            "id": sale.id,
            "interactor":{
                "id": sale.interactor.id,
                "name": sale.interactor.name
            },
            "created_at": sale.created_at,
            "created_by":{
                "id": sale.created_by.id,
                "name": sale.created_by.username
            },
            "sale_lines": sale_line,
            "total_quantity": sale.total_quantity,
            "total_amount": sale.total_amount        
        }
    
        return Response(sale_dict)


class Listsale(AuthRequiredApiView):
    def get(self, request):
        sale_list = Sale.objects.all().values('id', 'interactor__name', 'created_at', 'created_by','total_quantity', 'total_amount', )
       
        return Response(sale_list)



 