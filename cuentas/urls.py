from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("cuentas/", views.cuenta_view),
    path("movimientos/", views.movimiento_view),
]
