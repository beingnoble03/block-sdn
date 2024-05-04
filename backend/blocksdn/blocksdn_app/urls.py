from django.urls import path

from . import views

urlpatterns = [
    path("", views.controller_register, name="controller"),
    path("auth1/", views.controller_auth1, name="auth1"),
    path("auth2/", views.controller_auth2, name="auth2"),
]