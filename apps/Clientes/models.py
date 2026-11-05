from django.db import models

# Create your models here.

class clientes(models.Model):
    idCliente = models.AutoField(primary_key=True)
    idInfoPago = models.ForeignKey('Pagos.informacionPagos', on_delete=models.CASCADE)
    idDireccion = models.ForeignKey('direcciones', null=True, blank=True, on_delete=models.CASCADE)
    cNombre = models.CharField(max_length=30)
    cApellidoPaterno = models.CharField(max_length=30)
    cApellidoMaterno = models.CharField(max_length=30)
    cAlias = models.CharField(max_length=11, null=True, blank=True)
    cDetalle = models.CharField(max_length=15, null=True, blank=True)
    bActivo = models.BooleanField(default=True)

class sucursales(models.Model):
    idSucursal = models.AutoField(primary_key=True)
    idDireccion = models.ForeignKey('direcciones', on_delete=models.CASCADE, null=True, blank=True)
    cTitular = models.CharField(max_length=30)
    bActivo = models.BooleanField(default=True)

class direcciones(models.Model):
    idDireccion = models.AutoField(primary_key=True)
    idColonia = models.ForeignKey('colonias', null=True, blank=True, on_delete=models.CASCADE)
    idMunicipio = models.ForeignKey('municipios', null=True, blank=True, on_delete=models.CASCADE)
    idEstado = models.ForeignKey('estados', null=True, blank=True, on_delete=models.CASCADE)
    cCalle = models.CharField(max_length=20, null=True, blank=True)
    cNumero = models.CharField(max_length=3, null=True, blank=True)

class colonias(models.Model):
    idColonia = models.AutoField(primary_key=True)
    cColonia = models.CharField(max_length=20)
    
class municipios(models.Model):
    idMunicipio = models.AutoField(primary_key=True)
    cMunicipio = models.CharField(max_length=20)
    
class estados(models.Model):
    idEstado = models.AutoField(primary_key=True)
    cEstado = models.CharField(max_length=20)