from django.urls import path
from . import views

app_name = 'pagos'  # importante para usar el template tag automático

urlpatterns = [
    path('index/', views.indexPagos, name='indexPagos'),
]
