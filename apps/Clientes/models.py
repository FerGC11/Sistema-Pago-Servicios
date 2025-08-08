from django.db import models

# Create your models here.

class clientes(models.Model):
    idCliente = models.IntegerField(primary_key=True)
    idInfoPago = models.ForeignKey('Pagos.pagos', on_delete=models.CASCADE)
    idDireccion = models.ForeignKey('direcciones', on_delete=models.CASCADE)
    cNombre = models.CharField(max_length=30)
    cApellidoPaterno = models.CharField(max_length=30)
    cApellidoMaterno = models.CharField(max_length=30)
    cAlias = models.CharField(max_length=11, null=True, blank=True)
    cDetalle = models.CharField(max_length=15, null=True, blank=True)

class direcciones(models.Model):
    idDireccion = models.AutoField(primary_key=True)
    idColonia = models.ForeignKey('colonias', on_delete=models.CASCADE)
    idMunicipio = models.ForeignKey('municipios', on_delete=models.CASCADE)
    estados = models.ForeignKey('estados', on_delete=models.CASCADE)
    cCalle = models.CharField(max_length=20)
    cNumero = models.CharField(max_length=3, null=True,)
    
class colonias(models.Model):
    idColonia = models.AutoField(primary_key=True)
    cColonia = models.CharField(max_length=20)
    
class municipios(models.Model):
    idMunicipio = models.AutoField(primary_key=True)
    cMunicipio = models.CharField(max_length=20)
    
class estados(models.Model):
    idEstado = models.AutoField(primary_key=True)
    cEstado = models.CharField(max_length=20)