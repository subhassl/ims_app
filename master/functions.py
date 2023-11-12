from .models import Interactor

def getInteractorsFromDB():
    intercators = Interactor.objects.filter(is_active=True).values('id', 'name')
    return intercators