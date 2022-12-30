from django.urls import path

from .views import FacturaCompraView, GenerarFacturaView, FacturaListarView, FacturaVentaView, GenerarFacturaSalidaView

urlpatterns = [
    #compra
    path('generar/factura/compra/', FacturaCompraView.as_view(), name="factura_compra"),
    path('listar/factura/compra/', FacturaListarView.as_view(), name="listar_factura"),
    path('volante/pdf/<int:pk>/', GenerarFacturaView.as_view(), name="generar_factura"),
    #venta
    path('generar/factura/venta/', FacturaVentaView.as_view(), name="factura_venta"),
    path('volante/pdf/salida/<int:pk>/', GenerarFacturaSalidaView.as_view(), name="generar_factura_salida"),
]
