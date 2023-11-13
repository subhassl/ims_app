from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from master.views import AuthRequiredApiView
from .models import Purchase, PurchaseLine
from inventory.models import ItemStock 


"""
  request structure - (request)
    'interactor_id': 1,
    'lines': [
        {
            'item_id': 2,
            'quantity': 3, 
            'rate': 300
        },
        {
            'item_id': 1,
            'quantity': 4,
            'rate': 100
        },
    ]
}                           
"""               
class PurchaseView(AuthRequiredApiView):
    def post(self, request):
        try:
            with transaction.atomic():
                purchase_data = request.data
                # creating purchase in purchase table
                purchase = Purchase.objects.create(
                    interactor_id=purchase_data['interactor_id'],
                    created_by_id=request.user.id
                )

                # loop through lines array received in request data and create purchase line
                for line in purchase_data['lines']:
                    item_id = line['item_id']
                    quantity = line['quantity']
                    rate = line['rate']
                    amount = quantity * rate

                    # creating purchase line in purchase line table.
                    PurchaseLine.objects.create(
                        purchase_id=purchase.id,
                        item_id=item_id,
                        quantity=quantity,
                        rate=rate,
                        amount=amount
                    )

                    item_stock, is_created = ItemStock.objects.get_or_create(item_id=item_id)
                    item_stock.stock += quantity
                    item_stock.save()

                    # update total_quntity and total_amount in purchase object
                    purchase.total_quantity += quantity
                    purchase.total_amount += amount

                # save purchase object to update total qutity and total amount.  
                purchase.save()

                return Response({
                    "id": purchase.id
                })
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class PurchaseListView(AuthRequiredApiView):
    def get(self, request):
        purchases = Purchase.objects.all().values('id', 'interactor__name', 'created_at', 
        'created_by', 'total_quantity', 'total_amount',)

        res_dict = {
            "values": list(purchases)
        }

        return Response(res_dict)

class RetrivePurchaseData(AuthRequiredApiView):
    def get(self, request):
        purchase_id = request.GET.get('purchase_id')
        purchase = Purchase.objects.get(id=purchase_id)
        purchase_lines = PurchaseLine.objects.filter(purchase_id=purchase_id).values(
            'item_id', 'item__name', 'quantity', 'rate', 'amount',
        )        
        purchase_dict = {
            "id": purchase.id,
            "interactor": {
                "id": purchase.interactor.id,
                "name": purchase.interactor.name
            },
            "created_at": purchase.created_at,
            "created_by": {
                "id": purchase.created_by.id,
                "name": purchase.created_by.username
            },
            "line": purchase_lines,
            "total_quantity": purchase.total_quantity,
            "total_amount": purchase.total_amount
        }
        
        return Response(purchase_dict)
