from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ItemCategory, Item
from .functions import getInteractorsFromDB

class AuthRequiredApiView(APIView):
    authentication_classes = [TokenAuthentication]  # Specify the authentication class
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



