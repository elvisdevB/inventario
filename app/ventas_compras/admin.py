from pyexpat import model
from django.contrib import admin

from .models import FacturaEntrada, Entradas, FacturaSalidas, Salidas
# Register your models here.
class AdminFactura(admin.ModelAdmin):
    class Meta:
        model = FacturaEntrada

admin.site.register(FacturaEntrada, AdminFactura)

class AdminDetalle(admin.ModelAdmin):
    class Meta:
        model = Entradas

admin.site.register(Entradas, AdminDetalle)


class AdminFacturaSalida(admin.ModelAdmin):
    class Meta:
        model = FacturaSalidas

admin.site.register(FacturaSalidas, AdminFacturaSalida)

class AdminDetalleSalida(admin.ModelAdmin):
    class Meta:
        model = Salidas

admin.site.register(Salidas, AdminDetalleSalida)