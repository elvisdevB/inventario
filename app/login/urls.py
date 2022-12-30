import django

from django.urls import path

from .views import LoginFormView, LogoutFormView

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutFormView.as_view(), name="logout")
]
