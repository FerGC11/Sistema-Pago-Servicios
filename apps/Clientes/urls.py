from django.urls import path
from . import views

app_name = 'clientes'  # importante para usar el template tag automático

urlpatterns = [
    path('index/', views.indexClientes, name='indexClientes'),
]
