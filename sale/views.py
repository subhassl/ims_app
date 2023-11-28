from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from master.views import AuthRequiredApiView
from inventory.models import ItemStock 
from .models import Sale, SaleLine
from agent.models import Agent
import json
from django.db.models import Q
import datetime
from django.db.models import Sum, F 



# create Sale
class CreateSaleView(AuthRequiredApiView):

    def post(self, request):
        sale_data = request.data
        sale = Sale.objects.create(
            interactor_id=sale_data["interactor_id"],
            agent_id=sale_data["agent_id"],
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


class ItemCategoryReportByDate(AuthRequiredApiView):
    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))

            from_date = json_data.get('from_date', '')
            end_date = json_data.get('end_date', '')

            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            sale_line = SaleLine.objects.filter(
                sale__created_at__gte=from_date,
                sale__created_at__lte=end_date
            ).values(
                category_id=F("item__category_id"),
                category_name=F("item__category__name"),
                agent_name=F("sale__agent__name")
            ).annotate(
                totol_quantity=Sum("quantity"),
                total_amount=Sum("amount")
            )

            return Response(list(sale_line))
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        

class CustomerReportByDate(AuthRequiredApiView):
    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))

            from_date = json_data.get('from_date', '')
            end_date = json_data.get('end_date', '')

            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            sale = Sale.objects.filter(
                Q(created_at__gte=from_date) &
                Q(created_at__lte=end_date)
            ).values(
                'interactor_id','interactor__name', 
            ).annotate(
                total_quantity=Sum('total_quantity'),
                total_amount=Sum('total_amount')
            )

            return Response(list(sale))

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)






 