from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Cuenta, Transaccion
from functools import reduce
from logs.models import OperationLog


@login_required
@require_GET
def index(request):
    balance_list = [c.monto for c in
                    Cuenta.objects.using('default').filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO,
                                                           propietario=request.user)]
    balance_list.append(0)
    balance = reduce(lambda a, b: a + b, balance_list)

    cuentas = Cuenta.objects.using('default').filter(propietario=request.user)
    return render(request, "index.html", context={
        "balance": balance,
        "cuentas": cuentas,
        "seleccion": "index",
        "user": request.user
    })


@login_required
@require_http_methods(["GET", "POST"])
def cuenta_view(request):
    op = request.GET.get("op", "")
    context = {
        "op": op,
        "cuentas": Cuenta.objects.using('default').filter(propietario=request.user),
        "seleccion": "cuenta"
    }

    if op == "crear":
        context["tipos_cuenta"] = Cuenta.TipoCuenta.choices

    if request.method == "POST":
        user = request.user
        nombre = request.POST.get("nombre_cuenta")
        tipo = request.POST.get("tipo_cuenta")

        cuenta = Cuenta.objects.using('default').create(
            nombre=nombre,
            tipo=Cuenta.TipoCuenta(tipo),
            propietario=user,
        )

        cuenta.save()

        OperationLog.objects.using('logsdb').create(
            user_id=user.id,
            user_username=user.username,
            operation="Nueva cuenta. ID: " + str(cuenta.id)
        )

        return redirect("/cuentas")

    return render(request, "cuentas/cuentas.html", context=context)


@login_required
@require_http_methods(["GET", "POST"])
def movimiento_view(request):
    op = request.GET.get("op", "")
    user = request.user

    context = {
        "op": op,
        "movimientos": Transaccion.objects.using('default').filter(origen__propietario__id=user.id),
        "seleccion": "movimiento"
    }

    if op == "ingreso":
        context["cuentas_origen"] = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO)
        context["cuentas_destino"] = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO)

    if op == "gasto":
        context["cuentas_origen"] = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO)
        context["cuentas_destino"] = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.GASTO)

    if op == "traspaso":
        context["cuentas_origen"] = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO)
        context["cuentas_destino"] = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO)

    if request.method == "POST":
        cuenta_origen = request.POST.get("cuenta_origen")
        cuenta_destino = request.POST.get("cuenta_destino")
        monto = request.POST.get("monto")
        concepto = request.POST.get("concepto")
        fecha = request.POST.get("fecha")

        origen = Cuenta.objects.using('default').get(id=cuenta_origen)
        destino = Cuenta.objects.using('default').get(id=cuenta_destino)

        transaccion = Transaccion()
        transaccion.origen = origen
        transaccion.destino = destino
        transaccion.monto = float(monto)
        transaccion.concepto = concepto
        transaccion.fecha = fecha

        transaccion.realizar()

        OperationLog.objects.using('logsdb').create(
            user_id=user.id,
            user_username=user.username,
            operation="Nueva transaccion. ID: " + str(transaccion.id)
        )

        return redirect("/movimientos")

    return render(request, "movimientos/movimientos.html", context=context)
