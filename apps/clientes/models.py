from django.db import models

# Create your models here.


class direcciones(models.Model):
    idDireccion = models.AutoField(primary_key=True)
    cCalle = models.CharField(max_length=20)
    cNumero = models.CharField(max_length=3, null=True,)
    idColonia = models.ForeignKey('colonias', on_delete=models.CASCADE)
    idMunicipio = models.ForeignKey('municipios', on_delete=models.CASCADE)
    estados = models.ForeignKey('estados', on_delete=models.CASCADE)

class colonias(models.Model):
    idColonia = models.AutoField(primary_key=True)
    cColonia = models.CharField(max_length=20)
    
class municipios(models.Model):
    idMunicipio = models.AutoField(primary_key=True)
    cMunicipio = models.CharField(max_length=20)
    
class estados(models.Model):
    idEstado = models.AutoField(primary_key=True)
    cEstado = models.CharField(max_length=20)