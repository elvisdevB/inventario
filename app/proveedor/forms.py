from django import forms

from .models import Proveedor

class RegistrarProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['cod_proveedor','nombre','direccion','email','telefono','fecha_creacion']

        labels ={
            'cod_proveedor':'Codigo del Proveedor',
            'nombre':'Nombre de Proveedor',
            'direccion':'Direccion del Proveedor',
            'email':'Email del Proveedor',
            'telefono':'Telefono del Proveedor',
            'fecha_creacion':'Fecha de Registro',
        }

        widgets = {
            'cod_proveedor':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su Numero de Cedula'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su Nombre'}),
            'direccion':forms.Textarea(attrs={'class':'form-control','placeholder':'Ingrese su Direccion'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingrese su Email'}),
            'telefono':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su Numero de Telefono'}),
            'fecha_creacion':forms.DateInput(attrs={'class':'form-control','readonly':True}),
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