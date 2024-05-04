from django.urls import path

from . import views

urlpatterns = [
    path("", views.controller_register, name="controller"),
    path("auth/", views.controller_auth, name="auth")
]
