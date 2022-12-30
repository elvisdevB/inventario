from email.policy import default
from django.db import models
from app.proveedor.models import Proveedor
from django.forms.models import model_to_dict

from datetime import datetime

# Create your models here.
class Producto(models.Model):
    cod_producto = models.CharField(max_length=10, unique= True, null=False)
    cod_proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE)
    nombre = models.CharField(max_length = 250, null=False)
    precio_unitario = models.DecimalField( max_digits=10, decimal_places=2, null=False)
    fecha_creacion = models.DateField(default = datetime.now)

    def __str__(self):
        return self.cod_producto
    
    def toJson(self):
        item = model_to_dict(self)
        item['cod_producto'] = self.cod_producto
        item['cod_proveedor'] = self.cod_proveedor.cod_proveedor
        item['nombre'] = self.nombre
        item['precio_unitario'] = self.precio_unitario
        item['fecha_creacion'] = self.fecha_creacion
        return item

class Stock(models.Model):
    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False)
    cant_stock = models.IntegerField(null=False)
    fecha_ingreso = models.DateField(default=datetime.now)

    def __str__(self):
        return self.cod_producto
    
    def toJson(self):
        item = model_to_dict(self)
        item['cod_producto'] = self.cod_producto.nombre
        item['cant_stock'] = self.cant_stock
        item['fecha_ingreso'] = self.fecha_ingreso
        return item


    