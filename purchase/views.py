from rest_framework.response import Response
from master.views import AuthRequiredApiView
from .models import Purchase, PurchaseLine

class PurchaseView(AuthRequiredApiView):
    def post(self, request):
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

        purchase = Purchase.objects.create(
            interactor_id=purchase_data['interactor_id'],
            created_by_id=request.user.id
        )

        for line in purchase_data['lines']:
            item_id = line['item_id']
            quantity = line['quantity']
            rate = line['rate']
            amount = quantity * rate

            PurchaseLine.objects.create(
                purchase_id=purchase.id,
                item_id=item_id,
                quantity=quantity,
                rate=rate,
                amount=amount
            )

            purchase.total_quantity += quantity
            purchase.total_amount += amount
            
        purchase.save()

        return Response({
            "id": purchase.id
        })