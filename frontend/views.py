from django.shortcuts import render

def interactor_list(request):
    return render(request, 'interactor-list.html')

def create_interactor(request):
    return render(request, 'create-interactor.html')