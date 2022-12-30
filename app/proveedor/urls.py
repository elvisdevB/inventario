from django.urls import path
from .views import RegistrarProveedorView, ListarProveedoresView, EditarProveedorView, EliminarProveedorView

urlpatterns = [
    path('registrar/', RegistrarProveedorView.as_view(), name="registrar_proveedor"),
    path('listar/', ListarProveedoresView.as_view(), name="listar_proveedor"),
    path('listar/<int:pk>/', EditarProveedorView.as_view(), name="editar_proveedor"),
    path('eliminar/<int:pk>/', EliminarProveedorView.as_view(), name="eliminar_proveedor"),
]
