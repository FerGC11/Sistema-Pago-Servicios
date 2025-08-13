from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def indexPagos(request):
    return render(request, 'pagos/Pagos.html')