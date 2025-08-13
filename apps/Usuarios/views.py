from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def indexUsuarios(request):
    return render(request, 'usuarios/Usuarios.html')