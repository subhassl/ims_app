from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ItemCategory, Item, Interactor
from .functions import getInteractorsFromDB, getItemsFromDB
from django.shortcuts import render
import time


class AuthRequiredApiView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]  # Specify the authentication class
    permission_classes = [IsAuthenticated]  # Specify the permission class


class InteractorView(AuthRequiredApiView):

    def get(self, request):
        intercators = getInteractorsFromDB()
        
        res_dict = {
            "values": list(intercators),
            "count": intercators.count(),
        }

        return Response(res_dict)
    
    # def post(self, request):
    #     return Response({""})
class CreateInteractor(AuthRequiredApiView):
    
    def post(self,request):
        interactor_data = request.data

        # Validate the presence of required fields
        required_fields = ["name", "phone_number", "address"]
        for field in required_fields:
            if field not in interactor_data:
                return Response({"error": f"Missing required field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        # creating a interactor in Interactors table
        interactor = Interactor.objects.create(
            name=interactor_data["name"],
            phone_number=interactor_data["phone_number"],
            address=interactor_data["address"]
        )
        return Response( {
            "id": interactor.id
        } )

class GetItemView(AuthRequiredApiView):

    def get(self, request):
        item_id = request.GET.get("item_id")
        item = Item.objects.get(id=item_id)
        item_res = Item.objects.filter(id=item_id).values('name', 'item_code', 'category')
        return Response(item_res)




class CreateItem(AuthRequiredApiView):

    def post(self, request):
        item_data = request.data

        # creating a item in Interactors table
        item = Item.objects.create(
            name=item_data["name"],
            item_code=item_data["item_code"],
            category_id=item_data["category_id"]
        )

        return Response({
            "ïd": item.id
        })

class CreateItemCategory(AuthRequiredApiView):

    def post(self, request):
        item_category_data = request.data

        item_category = ItemCategory.objects.create(
            name=item_category_data["name"]
        )
        return Response(
            {
                "id": item_category.id            }
        )

class ItemCategoryView(AuthRequiredApiView):

    def get(self, request):
        item_categories = ItemCategory.objects.filter(is_active=True)
        res = []
        for ic in item_categories:
            ic_dict = {
                "id": ic.id,
                "name":ic.name,
            }

            res.append(ic_dict)
        
        return Response(data={
            "valus": res,
            "count":len(res)
        })


class ItemView(AuthRequiredApiView):
    def get(self, request):
        # Returns all items in all categories.
        items = getItemsFromDB()
        res_dict = {
            "values": list(items)
        }

        return Response(res_dict)


class UpdateItem(AuthRequiredApiView):
    
    def post(self, request):
        update_data = request.data
        item  = Item.objects.get(id=update_data["id"])

        new_name = update_data["name"]
        new_item_code = update_data["item_code"]
        new_category_id = update_data["category_id"]

        item.name = new_name
        item.item_code = new_item_code
        item.category_id = new_category_id

        item.save()

        return Response({
            "name": item.name
        })

class ListItemsInCategory(AuthRequiredApiView):
    def get(self, request):
        category_id = request.GET.get('category_id')
        item = Item.objects.filter(
            category_id=category_id
        ).values('id', 'name', 'item_code',)
        return Response({
            "values" : item
        })

class UpdateInteractor(AuthRequiredApiView):

    def post(self, request):
        update_data = request.data
        interactor = Interactor.objects.get(id=update_data['id'])

        # update the values based on user input
        new_name = update_data["name"]
        new_phone_number = update_data["phone_number"]
        new_address = update_data["address"]

        # update the interactor
        interactor.name = new_name  
        interactor.address = new_address
        interactor.phone_number = new_phone_number  

        interactor.save()

        return Response({
            "name": interactor.name
        })







    


