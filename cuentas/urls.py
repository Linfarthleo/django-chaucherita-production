from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("cuentas/", views.CuentaView.as_view()),
    path("movimientos/", views.MovimientoView.as_view()),
]
