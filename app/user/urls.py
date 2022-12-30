from django.urls import path

from .views import RegistrarUsuarioView, CrearUsuarioView, UsuarioListarView, GroupView, EditarUsuarioView

urlpatterns = [
    path('registrar/', RegistrarUsuarioView.as_view(), name="registrar_usuario" ),
    path('crear/usuario/', CrearUsuarioView.as_view(), name="crear_usuario" ),
    path('lista/usuarios/', UsuarioListarView.as_view(), name="listar_usuarios" ),
    path('editar/usuarios/<int:pk>/', EditarUsuarioView.as_view(), name="editar_usuarios"),
    path('change/group/<int:pk>/', GroupView.as_view(), name="usuario_cambiar_grupos"),
]

