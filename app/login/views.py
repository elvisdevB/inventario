from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from inventario.settings.base import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
# Create your views here.

class LoginFormView(LoginView):
    template_name = "login.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Iniciar Sesion"
        return context


class LogoutFormView(RedirectView):
    pattern_name = LOGOUT_REDIRECT_URL

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Ha salido del Sistema")
        return super().dispatch(request, *args, **kwargs)
