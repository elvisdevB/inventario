from pyexpat import model
from django.contrib import admin

from .models import Producto
# Register your models here.
class AdminProducto(admin.ModelAdmin):
    class Meta:
        model = Producto

admin.site.register(Producto,AdminProducto)
