from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from master.views import AuthRequiredApiView
from .models import Purchase, PurchaseLine

class PurchaseView(AuthRequiredApiView):
    def post(self, request):
        try:
            with transaction.atomic():
                purchase_data = request.data
                """
                request structure
                {
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