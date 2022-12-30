from django.urls import path

from .views import CrearProductoView, ListarProductosView, EditarProductoView

urlpatterns = [
    path('registrar/', CrearProductoView.as_view(), name="registrar_producto"),
    path('listar/', ListarProductosView.as_view(), name="listar_productos"),
    path('editar/<int:pk>/', EditarProductoView.as_view(), name="editar_producto"),
]
