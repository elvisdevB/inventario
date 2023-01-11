from django.db import models
from django.forms.models import model_to_dict

from app.producto.models import Producto
from app.proveedor.models import Proveedor
from datetime import datetime

# Create your models here.
class FacturaEntrada(models.Model):
    cod_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField( max_digits=10, decimal_places=2)
    fecha_emision = models.DateField(default = datetime.now)

    def __str__(self):
        return self.cod_proveedor.nombre
    
    def toJson(self):
        item = model_to_dict(self)
        item['cod_proveedor'] = self.cod_proveedor.cod_proveedor
        item['subtotal'] = format(self.subtotal,'.2f')
        item['iva'] = format(self.iva,'.2f')
        item['total'] = format(self.total,'.2f')
        item['fecha_emision'] = self.fecha_emision
        return item

class Entradas(models.Model):
    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False)
    cod_factura = models.ForeignKey(FacturaEntrada, on_delete=models.CASCADE, null=False)
    cantidad_ingreso_stock = models.IntegerField(null=False)
    subtotal = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField(default= datetime.now)

    def __str__(self):
        return self.cod_factura.cod_proveedor.nombre

    def toJson(self):
        item = model_to_dict(self)
        item['cod_producto'] = self.cod_producto.toJson()
        item['cantidad_ingreso_stock'] = self.cantidad_ingreso_stock
        item['fecha_ingreso'] = self.fecha_ingreso
        return item


class FacturaSalidas(models.Model):
    cod_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField( max_digits=10, decimal_places=2)
    fecha_emision = models.DateField(default = datetime.now)

    def __str__(self):
        return self.cod_proveedor.nombre
    
    def toJson(self):
        item = model_to_dict(self)
        item['cod_proveedor'] = self.cod_proveedor.cod_proveedor
        item['subtotal'] = format(self.subtotal,'.2f')
        item['iva'] = format(self.iva,'.2f')
        item['total'] = format(self.total,'.2f')
        item['fecha_emision'] = self.fecha_emision
        return item

class Salidas(models.Model):
    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False)
    cod_factura = models.ForeignKey(FacturaSalidas, on_delete=models.CASCADE, null=False)
    cantidad_salida_stock = models.IntegerField(null=False)
    subtotal = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    fecha_salida = models.DateField(default= datetime.now)

    def __str__(self):
        return self.cod_factura.cod_proveedor.nombre

    def toJson(self):
        item = model_to_dict(self)
        item['cod_producto'] = self.cod_producto.toJson()
        item['cantidad_salida_stock'] = self.cantidad_salida_stock
        item['fecha_salida'] = self.fecha_salida
        return item
