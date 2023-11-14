from .models import Interactor, Item

def getInteractorsFromDB():
    intercators = Interactor.objects.filter(is_active=True).values('id', 'name')
    return intercators


def getItemsFromDB():
    items = Item.objects.filter(is_active=True).values('id', 'name', 'item_code')
    return items
    