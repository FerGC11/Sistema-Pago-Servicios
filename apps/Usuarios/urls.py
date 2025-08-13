from django.urls import path
from . import views

app_name = 'usuarios'  # importante para usar el template tag automático

urlpatterns = [
    path('index/', views.indexUsuarios, name='indexUsuarios'),
]
