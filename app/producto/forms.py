from django import forms
from datetime import datetime

from .models import Producto
from app.proveedor.models import Proveedor

class RegistrarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = {'cod_producto','cod_proveedor','nombre','precio_unitario','stock','imagen'}

        labels = {
            'cod_producto':'Ingrese el Codigo del Producto',
            'cod_proveedor':'Seleccione el Proveedor',
            'nombre':'Ingrese el nombre del Producto',
            'precio_unitario':'Ingrese el Precio unitario del Producto',
            'stock':'Ingrese el Stock total del Producto',
            'imagen':'Ingrese la imagen del Producto'
        }

        widgets = {
            'cod_producto':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese Codigo Producto'}),
            'cod_proveedor':forms.Select(attrs={'class':'form-select select2'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre de Producto'}),
            'precio_unitario': forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese el precio del Producto'}),
            'stock':forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese el stock del Producto'}),
            'imagen':forms.FileInput(attrs={'class':'form-control','placeholder':'Ingrese la imagen del Producto'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cod_proveedor'].queryset = Proveedor.objects.none()
    

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = {'cod_producto','cod_proveedor','nombre','precio_unitario','stock'}

        labels = {
            'cod_producto':'Ingrese el Codigo del Producto',
            'cod_proveedor':'Seleccione el Proveedor',
            'nombre':'Ingrese el nombre del Producto',
            'precio_unitario':'Ingrese el Precio unitario del Producto',
            'stock':'Ingrese el Stock total del Producto'
        }

        widgets = {
            'cod_producto':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese Codigo Producto'}),
            'cod_proveedor':forms.Select(attrs={'class':'form-select select2'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre de Producto'}),
            'precio_unitario': forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese el precio del Producto'}),
            'stock':forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese el stock del Producto'})
        }
    