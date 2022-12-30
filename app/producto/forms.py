from django import forms
from datetime import datetime

from .models import Producto
from app.proveedor.models import Proveedor

class RegistrarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = {'cod_producto','cod_proveedor','nombre','precio_unitario','fecha_creacion'}

        labels = {
            'cod_producto':'Ingrese el Codigo del Producto',
            'cod_proveedor':'Seleccione el Proveedor',
            'nombre':'Ingrese el nombre del Producto',
            'precio_unitario':'Ingrese el Precio unitario del Producto',
            'fecha_creacion':'Fecha de Creacion del Producto'
        }

        widgets = {
            'cod_producto':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese Codigo Producto'}),
            'cod_proveedor':forms.Select(attrs={'class':'form-select select2'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre de Producto'}),
            'precio_unitario': forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese el precio del Producto'}),
            'fecha_creacion':forms.DateInput(format="%Y-%m-%d",attrs={'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cod_proveedor'].queryset = Proveedor.objects.none()
    

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = {'cod_producto','nombre','precio_unitario','fecha_creacion'}

        labels = {
            'cod_producto':'Ingrese el Codigo del Producto',
            'nombre':'Ingrese el nombre del Producto',
            'precio_unitario':'Ingrese el Precio unitario del Producto',
            'fecha_creacion':'Fecha de Creacion del Producto'
        }

        widgets = {
            'cod_producto':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese Codigo Producto'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre de Producto'}),
            'precio_unitario': forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese el precio del Producto'}),
            'fecha_creacion':forms.DateInput(format="%Y-%m-%d",attrs={'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control'})
        }
    
    def save(self, commit = True):
        data = {}
        form = super()
        if form.is_valid():
            instance = form.save()
            data = instance.toJson()
        else:
            data['error'] = form.errors
        return data