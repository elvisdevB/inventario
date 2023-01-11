
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from .models import Proveedor
from .forms import RegistrarProveedorForm
from app.user.mixins import ValidatePermissionRequiredMixin

# Create your views here.

class IndexView(LoginRequiredMixin ,TemplateView):
    template_name = "index.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

class RegistrarProveedorView(ValidatePermissionRequiredMixin, LoginRequiredMixin,CreateView):
    model = Proveedor
    form_class = RegistrarProveedorForm
    template_name = "registrar_proveedor.html"
    permission_required= 'add_proveedor'
    success_url = reverse_lazy('listar_proveedor')

    def post(self, request,*args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                proveedor = Proveedor()
                proveedor.cod_proveedor = request.POST.get('cod_proveedor')
                proveedor.nombre = request.POST.get('nombre')
                proveedor.direccion = request.POST.get('direccion')
                proveedor.email = request.POST.get('email')
                proveedor.telefono = request.POST.get('telefono')
                proveedor.save()
                messages.success(request, "Se ha Registrado con exito")
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Proveedores"
        context['success_url'] = self.success_url
        context['cancel_url'] = reverse_lazy('listar_proveedor')
        return context

class ListarProveedoresView(ValidatePermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = "listar_proveedor.html"
    permission_required= 'view_proveedor'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'listar_proveedores':
                data = []
                for i in Proveedor.objects.all():
                    data.append(i.toJson())
            elif action == 'delete':
                proveedor = Proveedor.objects.get(pk = request.POST['id'] )
                proveedor.delete()
                messages.success(request, "Proveedor eliminado con Exito")
            else:
                data['error'] = "No ha ingresado ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Lista de Proveedores"
        context['list_actualizar'] = reverse_lazy('listar_proveedor')
        return context

class EditarProveedorView(ValidatePermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = RegistrarProveedorForm
    template_name = "editar_proveedor.html"
    permission_required= 'change_proveedor'
    success_url = reverse_lazy('listar_proveedor')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                proveedor = Proveedor.objects.get(pk = kwargs['pk'])
                proveedor.cod_proveedor = request.POST.get('cod_proveedor')
                proveedor.nombre = request.POST.get('nombre')
                proveedor.direccion = request.POST.get('direccion')
                proveedor.email = request.POST.get('email')
                proveedor.telefono = request.POST.get('telefono')
                proveedor.save()
                messages.success(request, "Proveedor Editado con exito")
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Proveedor"
        context['mensaje_informacion'] = "¿ Seguro de Editar este registro ?"
        context['success_url'] = self.success_url
        context['cancel_url'] = reverse_lazy('listar_proveedor')
        return context

