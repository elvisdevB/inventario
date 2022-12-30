from pyexpat import model
from django.contrib import admin
from .models import Proveedor

# Register your models here.

class AdminProveedor(admin.ModelAdmin):
    class Meta:
        model = Proveedor

admin.site.register(Proveedor,AdminProveedor)
