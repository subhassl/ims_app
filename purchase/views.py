from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from master.views import AuthRequiredApiView
from .models import Purchase, PurchaseLine
from inventory.models import ItemStock 
from django.db.models import Q
import json
import datetime
from django.db.models import Sum


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




# repots based on data range

class FetchPurchaseDataBasedOnDate(AuthRequiredApiView):
    def post(self, request):
        try:
            # Load JSON data from the request body
            '''
            1. Json_data now holds a Python dictionary representing 
            the JSON data sent in the request body.

            '''
            json_data = json.loads(request.body.decode('utf-8'))

            from_date = json_data.get('from_date', '')
            end_date = json_data.get('end_date', '')

            # Convert string dates to actual date objects
            '''
            strptime method from the datetime module to parse a string (start_date) into a datetime object.
            Putting it all together, these lines of code take a string representing a date (start_date and end_date) 
            and convert it into a date object in Python.
            '''
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            # Fetch purchases within the date range
            # Q(...): This is a Django object used to encapsulate a query expression.
            # It's often used when you want to build complex queries with logical operations like AND (&), OR (|), and NOT (~).
            purchases = Purchase.objects.filter(
                Q(created_at__gte=from_date) &
                Q(created_at__lte=end_date)
            )

            # build a list of dictionaries
            report = []
            for purchase in purchases:
                our_data = {
                    "interactor": purchase.interactor.name,
                    "total_quantity": purchase.total_quantity,
                    "total_amount": purchase.total_amount
                }
                report.append(our_data)

            res = {}
            for indv in report:
                interactor = indv["interactor"] # interactor = pothys
                if interactor not in res:
                    res[interactor] = {
                        "total_quantity": 0,
                        "total_amount": 0 
                    }
                res[interactor]["total_quantity"] += indv["total_quantity"]
                res[interactor]["total_amount"] += indv["total_amount"]

            res_list = [
                        {"interactor": key, **value} for key, value in res.items()
                ]

            

            return Response(
                 res_list
            )
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    
class ItemCategoryReportByDate(AuthRequiredApiView):
    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))

            from_date = json_data.get('from_date', '')
            end_date = json_data.get('end_date', '')

            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            purchase_lines = PurchaseLine.objects.filter(
                purchase__created_at__gte=from_date,
                purchase__created_at__lte=end_date,
            ).values(
                "item__category_id",
                "item__category__name",
            ).annotate(
                total_quantity=Sum("quantity"), 
                total_amount=Sum("amount")
            )

            return Response(list(purchase_lines))
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)








