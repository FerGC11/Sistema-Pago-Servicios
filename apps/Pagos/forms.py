from django import forms
from .models import pagos, informacionPagos
from apps.Clientes.models import clientes, direcciones

class PagoForm(forms.ModelForm):
    class Meta:
        model = pagos
        fields = [
            'idInfoPago', 
            'importe',
            'idEstadoPago', 
        ]

class InformacionPagoForm(forms.ModelForm):
    class Meta:
        model = informacionPagos
        fields = [
            'iReferencia', 
            'iImporte', 
            'dFechaCorte'
        ]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = clientes
        fields = [
            'cNombre', 
            'cApellidoPaterno', 
            'cApellidoMaterno', 
            'cAlias', 
            'cDetalle', 
        ]

class DireccionForm(forms.ModelForm):
    class Meta:
        model = direcciones
        fields = [
            'idColonia', 
            'idMunicipio', 
            'idEstado', 
            'cCalle', 
            'cNumero'
        ]