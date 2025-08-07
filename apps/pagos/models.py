from django.db import models

# Create your models here.


class estatusPagos(models.Model):
    idEstatusPago = models.AutoField(primary_key=True)
    cEstatusPago = models.CharField(max_length=9)

class estadosPagos(models.Model):
    idEstadoPago = models.AutoField(primary_key=True)
    cEstadoPago = models.CharField(max_length=8)
    