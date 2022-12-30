import json
from urllib import request
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Producto, Stock
from app.proveedor.models import Proveedor
from .forms import RegistrarProductoForm, EditarProductoForm
from app.user.mixins import ValidatePermissionRequiredMixin

# Create your views here.

class CrearProductoView(ValidatePermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Producto
    form_class = RegistrarProductoForm
    template_name = 'registrar_producto.html'
    permission_required= 'add_producto'
    success_url = reverse_lazy('listar_productos')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "buscarproveedor":
                data = []
                proveedor = Proveedor.objects.filter(cod_proveedor__icontains = request.POST['term'])[0:10]
                for i in proveedor:
                    item = i.toJson()
                    item['text'] = i.cod_proveedor
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    productoItem = json.loads(request.POST['producto'])
                    print(productoItem)
                    producto = Producto()
                    producto.cod_producto = productoItem['cod_producto']
                    producto.cod_proveedor_id = productoItem['cod_proveedor']
                    producto.nombre = productoItem['nombre']
                    producto.precio_unitario = productoItem['precio_unitario']
                    producto.fecha_creacion = productoItem['fecha_creacion']
                    producto.save()

                    #Stock
                    stock = Stock()
                    stock.cod_producto_id = producto.id
                    stock.cant_stock = productoItem['cant_stock']
                    stock.save()
                    messages.success(request, "Producto Guardado con exito")
                    
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['titulo'] = "Registrar Producto"
        context['success_url'] = self.success_url
        context['cancel_url'] = reverse_lazy('index')
        return context

class ListarProductosView(ValidatePermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Producto
    template_name = "listar_productos.html"
    permission_required= 'view_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'verProductos':
                data= []
                for i in Producto.objects.all():
                    data.append(i.toJson())
            elif action == 'ver_stock':
                data = []
                for i in Stock.objects.filter(cod_producto=request.POST['id']):
                    data.append(i.toJson())
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Lista de Productos"
        context['list_actualizar'] = reverse_lazy('listar_productos')
        return context    

class EditarProductoView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = EditarProductoForm
    template_name = "editar_producto.html"
    success_url = reverse_lazy('listar_productos')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "edit":
                producto = Producto.objects.get(pk = kwargs['pk'])
                producto.cod_producto = request.POST.get('cod_producto')
                producto.save()
                messages.success(request, "Producto editado con Exito")
            else:
                data['error'] = "Ha ocurrido un error"

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = "edit"
        context['titulo'] = "Editar Producto"
        context['success_url'] = self.success_url
        context['cancel_url'] = reverse_lazy('listar_productos')
        return context
