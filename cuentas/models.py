from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from math import fabs

# Create your models here.
class Cuenta(models.Model):
    class TipoCuenta(models.TextChoices):
        INGRESO_EGRESO = 'IE', 'Ingreso y Gasto'
        INGRESO = 'I', 'Ingreso'
        GASTO = 'E', 'Gasto'

    nombre = models.CharField(max_length=60)
    monto = models.FloatField(default=0.0)
    tipo = models.CharField(max_length=3, default=TipoCuenta.INGRESO_EGRESO, choices=TipoCuenta.choices)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)

    def set_monto(self, monto):
        if self.tipo == Cuenta.TipoCuenta.INGRESO:
            self.monto += fabs(monto)
        elif self.tipo == Cuenta.TipoCuenta.GASTO:
            self.monto -= fabs(monto)
        else:
            self.monto += monto


class Transaccion(models.Model):
    origen = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='cuenta_origen')
    destino = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='cuenta_destino')
    fecha = models.DateField()
    monto = models.FloatField()
    concepto = models.TextField()

    def realizar(self):

        self.origen.set_monto(-self.monto)
        self.destino.set_monto(self.monto)

        self.origen.save()
        self.destino.save()

        self.save()

