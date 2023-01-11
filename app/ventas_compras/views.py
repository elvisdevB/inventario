from urllib import request, response
from django import forms
from django.shortcuts import render
from django.views.generic import CreateView, View, ListView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.contrib import messages
from django.template.loader import  get_template
from django.contrib.auth.mixins import LoginRequiredMixin

import json
from xhtml2pdf import pisa

from app.producto.models import Producto
from app.proveedor.models import Proveedor

from .models import FacturaEntrada, Entradas, FacturaSalidas, Salidas
from .forms import CompraFacturaForm
from app.user.mixins import ValidatePermissionRequiredMixin
# Create your views here.

#Compras
class FacturaCompraView(ValidatePermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = FacturaEntrada
    form_class = CompraFacturaForm
    template_name = "compra/compra_factura.html"
    permission_required= 'add_facturaentrada'
    success_url = reverse_lazy('index')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "buscarProductos":
                data = []
                producto = Producto.objects.filter(nombre__icontains = request.POST['term'])[0:10]
                for i in producto:
                    item = i.toJson()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == "buscarProveedor":
                data = []
                proveedor = Proveedor.objects.filter(cod_proveedor__icontains = request.POST['term'])[0:10]
                for i in proveedor:
                    item = i.toJson()
                    item['text'] = i.cod_proveedor
                    data.append(item)
            elif action == "add":
                with transaction.atomic():
                    factura_data = json.loads(request.POST['compra'])
                    factura = FacturaEntrada()
                    factura.cod_proveedor_id = factura_data['cod_proveedor']
                    factura.subtotal = float(factura_data['subtotal'])
                    factura.iva = float(factura_data['iva'])
                    factura.total = float(factura_data['total'])
                    factura.fecha_emision = factura_data['fecha_emision']
                    factura.save()

                    for i in factura_data['producto']:
                        entrada = Entradas()
                        entrada.cod_producto_id = i['id']
                        entrada.cod_factura_id = factura.id
                        entrada.cantidad_ingreso_stock = i['cantidad']
                        entrada.subtotal = i['subtotal']
                        entrada.fecha_ingreso = factura_data['fecha_emision']
                        entrada.save()

                        stock_antiguo = Producto.objects.get(pk=i['id'])
                        stock_antiguo.stock = stock_antiguo.stock + i['cantidad']
                        stock_antiguo.save()

                    data = {'id':factura.id}

                    messages.success(request, "Compra realizada con Exito")

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Factura Compra"
        context['action'] = 'add'
        return context


class FacturaListarView(ValidatePermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = FacturaEntrada
    template_name = "compra/listar_factura.html"
    permission_required= 'view_facturaentrada'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "listar_factura":
                data = []
                for i in FacturaEntrada.objects.all():
                    data.append(i.toJson())
            elif action == "ver_detalle_compra":
                data = []
                for i in Entradas.objects.filter(cod_factura=request.POST['id']):
                    data.append(i.toJson())
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class GenerarFacturaView(LoginRequiredMixin, View):

    def get(self, request,*args, **kwargs):
        try:
            template = get_template("compra/generar_factura.html")

            context = {
                'sale': FacturaEntrada.objects.get(pk=self.kwargs['pk']),
                'comp':{'name':'ElvisSOFT', 'ruc':'099999999999','address':'Milagro Ecuador'}
            }

            html = template.render(context)
            response = HttpResponse(content_type = "application/pdf")

            pisaStatus = pisa.CreatePDF(
                html, dest = response
            )
            
            if pisaStatus.err:
                return HttpResponse("Error <pre>" + html +"</pre>")
            return response
            
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(reverse_lazy("index"))


#Ventas
class FacturaVentaView(ValidatePermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = FacturaSalidas
    form_class = CompraFacturaForm
    template_name = "venta/venta_factura.html"
    permission_required= 'add_facturasalidas'
    success_url = reverse_lazy('index')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "buscarProductos":
                data = []
                producto = Producto.objects.filter(nombre__icontains = request.POST['term'])[0:10]
                for i in producto:
                    item = i.toJson()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == "buscarProveedor":
                data = []
                proveedor = Proveedor.objects.filter(cod_proveedor__icontains = request.POST['term'])[0:10]
                for i in proveedor:
                    item = i.toJson()
                    item['text'] = i.cod_proveedor
                    data.append(item)
            elif action == "add":
                with transaction.atomic():
                    factura_data = json.loads(request.POST['compra'])
                    factura = FacturaSalidas()
                    factura.cod_proveedor_id = factura_data['cod_proveedor']
                    factura.subtotal = float(factura_data['subtotal'])
                    factura.iva = float(factura_data['iva'])
                    factura.total = float(factura_data['total'])
                    factura.fecha_emision = factura_data['fecha_emision']
                    factura.save()

                    for i in factura_data['producto']:
                        entrada = Salidas()
                        entrada.cod_producto_id = i['id']
                        entrada.cod_factura_id = factura.id
                        entrada.cantidad_salida_stock = i['cantidad']
                        entrada.subtotal = i['subtotal']
                        entrada.fecha_salida = factura_data['fecha_emision']
                        entrada.save()

                        stock_antiguo = Producto.objects.get(pk=i['id'])
                        if(i['cantidad'] >= stock_antiguo.stock):
                            raise forms.ValidationError("La cantidad solicitada sobrepasa el stock del producto " + stock_antiguo.nombre)
                        stock_antiguo.stock = stock_antiguo.stock - i['cantidad']
                        stock_antiguo.save()
                        """ stock_antiguo = Stock.objects.filter(cod_producto_id=i['id']).last()
                        print(i['cantidad'])
                        if(i['cantidad'] >= stock_antiguo.cant_stock):
                            raise forms.ValidationError("La cantidad solicitada sobrepasa el stock del producto " + stock_antiguo.cod_producto.nombre)
                        stock_nuevo = Stock()
                        stock_nuevo.cod_producto_id = i['id']
                        stock_nuevo.cant_stock = stock_antiguo.cant_stock - i['cantidad']
                        stock_nuevo.save() """

                    data = {'id':factura.id}

                    messages.success(request, "Compra realizada con Exito")
            
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Factura de Venta"
        context['action'] = 'add'
        return context


class GenerarFacturaSalidaView(LoginRequiredMixin, View):
    def get(self, request,*args, **kwargs):
        try:
            template = get_template("venta/generar_factura.html")

            context = {
                'sale': FacturaSalidas.objects.get(pk=self.kwargs['pk']),
                'comp':{'name':'ElvisSOFT', 'ruc':'099999999999','address':'Milagro Ecuador'}
            }

            html = template.render(context)
            response = HttpResponse(content_type = "application/pdf")

            pisaStatus = pisa.CreatePDF(
                html, dest = response
            )
            
            if pisaStatus.err:
                return HttpResponse("Error <pre>" + html +"</pre>")
            return response
            
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(reverse_lazy("index"))