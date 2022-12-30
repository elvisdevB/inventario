from django import forms

from.models import FacturaEntrada
from app.proveedor.models import Proveedor
from datetime import datetime


class CompraFacturaForm(forms.ModelForm):
    class Meta:
        model = FacturaEntrada
        fields = ['cod_proveedor','subtotal','iva','total','fecha_emision']

        labels = {
            'cod_proveedor':'Buscar Proveedor',
            'iva':'IVA',
            'subtotal':'Subtotal',
            'total':'Total a Pagar',
            'fecha_emision':'Fecha de Creacion de Factura'
        }

        widgets = {
            'cod_proveedor':forms.Select(attrs={'class':'form-control select2'}),
            'iva':forms.NumberInput(attrs={'class':'form-control','readonly':True}),
            'subtotal':forms.NumberInput(attrs={'class':'form-control','readonly':True}),
            'total':forms.NumberInput(attrs={'class':'form-control','readonly':True}),
            'fecha_emision':forms.DateInput(format="%Y-%m-%d",
												attrs={
													'value':datetime.now().strftime('%Y-%m-%d'),
													'autocomplete':'off',
													'class':'form-control datetimepicker-input',
													'id':'date_joined',
													'data-target':'#date_joined',
													'data-toggle':'datetimepicker'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cod_proveedor'].queryset = Proveedor.objects.none()

