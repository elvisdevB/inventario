import imp
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView ,ListView, View
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

from .models import User
from .forms import FormRegistrarUser, CrearUsuarioForm
from app.user.mixins import ValidatePermissionRequiredMixin

# Create your views here.

class RegistrarUsuarioView(CreateView):
    model = User
    form_class = CrearUsuarioForm
    template_name = "registrar_usuario.html"
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "add":
                form = self.get_form()
                data = form.save()
                messages.success(request, "Usuario creado con Exito")
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['success_url'] = self.success_url
        return context

class CrearUsuarioView(ValidatePermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = FormRegistrarUser
    template_name = "crear_usuario.html"
    permission_required= 'add_user'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "add":
                form = self.get_form()
                data = form.save()
                messages.success(request, "Usuario creado con Exito")
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['cancel_url'] = reverse_lazy('listar_usuarios')
        context['success_url'] = self.success_url
        return context

class UsuarioListarView(ValidatePermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = "listar_usuarios.html"
    permission_required= 'view_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "buscar_usuarios":
                data = []
                for i in User.objects.all():
                    data.append(i.toJson())
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class EditarUsuarioView(ValidatePermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = FormRegistrarUser
    template_name = "crear_usuario.html"
    permission_required= 'change_user'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "edit":
                form = self.get_form()
                data = form.save()
                messages.success(request, "Usuario Editado con Exito")
            else:
                data['error'] = "No ha elejido ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = "edit"
        context['success_url'] = reverse_lazy('listar_usuarios')
        return context

class GroupView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('index'))