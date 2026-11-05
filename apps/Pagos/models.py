from django.db import models

# Create your models here.

class pagos(models.Model):
    idPago = models.AutoField(primary_key=True)
    idInfoPago = models.ForeignKey('informacionPagos', on_delete=models.CASCADE)
    idEstatusPago = models.ForeignKey('estatusPagos', on_delete=models.CASCADE)
    idEstadoPago = models.ForeignKey('estadosPagos', on_delete=models.CASCADE)
    importe = models.IntegerField(null=True, blank=True)
    dFechaPago = models.DateField()

class informacionPagos(models.Model):
    idInfoPago = models.AutoField(primary_key=True)
    iReferencia = models.IntegerField(null=True, blank=True)
    iImporte = models.IntegerField(null=True, blank=True)
    dFechaCorte = models.DateField(null=True, blank=True)
    
class estatusPagos(models.Model):
    idEstatusPago = models.AutoField(primary_key=True)
    cEstatusPago = models.CharField(max_length=9)

class estadosPagos(models.Model):
    idEstadoPago = models.AutoField(primary_key=True)
    cEstadoPago = models.CharField(max_length=8)

