from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE


# Create your models here.

class CustomUser(AbstractUser):
    #nuevos campos
    idSucursal = models.ForeignKey('Clientes.sucursales', on_delete=CASCADE, blank=True, null=True)
    idTipoUsuario = models.ForeignKey('TiposUsuarios', on_delete=CASCADE, blank=True, null=True)

    #Campos actualizados
    email = models.EmailField(blank=True, null=True)     
    last_name = models.CharField(max_length=20, blank=True, null=True) 

    #nuevo campo
    bActivo = models.BooleanField(default=True)

class TiposUsuarios(models.Model):
    idTipoUsuario = models.AutoField(primary_key=True)
    cTipoUsuario = models.CharField(max_length=6)