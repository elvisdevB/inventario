from datetime import datetime
from django.db import models
from django.forms.models import model_to_dict

# Create your models here.

class Proveedor(models.Model):
    cod_proveedor = models.CharField(max_length=10, unique=True, null=False)
    nombre = models.CharField(max_length=250, null=False)
    direccion = models.TextField(max_length=250, null=False)
    email = models.EmailField(max_length=300, null=False)
    telefono = models.CharField(max_length=10, null=False)
    fecha_creacion = models.DateField(default=datetime.now)

    def __str__(self):
        return self.cod_proveedor
    
    def toJson(self):
        item = model_to_dict(self)
        item['cod_proveedor'] = self.cod_proveedor
        item['nombre'] = self.nombre
        item['direccion'] = self.direccion
        item['email'] = self.email
        item['telefono'] = self.telefono
        item['fecha_creacion'] = self.fecha_creacion
        return item