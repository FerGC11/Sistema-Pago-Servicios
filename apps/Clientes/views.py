from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def indexClientes(request):
    return render(request, 'clientes/Clientes.html')
