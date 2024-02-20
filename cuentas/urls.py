from django.urls import path
from . import views
from .views import CuentaView, MovimientoView

urlpatterns = [
    path("", views.index),
    path("cuentas/", CuentaView.as_view()),
    path("movimientos/", MovimientoView.as_view()),
]
