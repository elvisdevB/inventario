from django.urls import path
from .views import RegistrarProveedorView, ListarProveedoresView, EditarProveedorView

urlpatterns = [
    path('registrar/', RegistrarProveedorView.as_view(), name="registrar_proveedor"),
    path('listar/', ListarProveedoresView.as_view(), name="listar_proveedor"),
    path('listar/<int:pk>/', EditarProveedorView.as_view(), name="editar_proveedor")
]
