from django.urls import path
from . import views

app_name = 'pagos'  # importante para usar el template tag automático

urlpatterns = [
    path("detalle-pago/<int:pago_id>/", views.detallePago, name="detallePago"),
    path("confirmar-pago/", views.confirmarPago, name="confirmarPago"),
    path('index/', views.indexPagos, name='indexPagos'),
    path('registrar-servicio/', views.registrarServicio, name='registrarServicio'),
    path('buscar-clientes/', views.buscarCliente, name='buscarCliente'),
    path('registrar-pago/', views.registrarPago, name='registrarPago'),
]
