from django.db import models

# Create your models here.

class colonias(models.Model):
    idColonia = models.AutoField(primary_key=True)
    cColonia = models.CharField(max_length=20)
    
class municipios(models.Model):
    idMunicipio = models.AutoField(primary_key=True)
    cMunicipio = models.CharField(max_length=20)
    
class estados(models.Model):
    idEstado = models.AutoField(primary_key=True)
    cEstado = models.CharField(max_length=20)