from django.utils.html import escape
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods

from .forms import CrearCuentaForm, MovimientoForm
from .models import Cuenta, Transaccion
from functools import reduce
from logs.models import OperationLog


@login_required
@require_GET
def index(request):

    if (len(request.GET) > 0):
        return redirect("/")
    
    balance_list = [c.monto for c in
                    Cuenta.objects.using('default').filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO,
                                                           propietario=request.user)]
    balance_list.append(0)
    balance = reduce(lambda a, b: a + b, balance_list)

    cuentas = Cuenta.objects.filter(propietario=request.user)
    return render(request, "index.html", context={
        "balance": balance,
        "cuentas": cuentas,
        "seleccion": "index",
        "user": request.user
    })


@login_required
@require_http_methods(["GET", "POST"])
def cuenta_view(request):
    
    form = CrearCuentaForm(request.POST)
    message = ""
    op = request.GET.get("op")

    if len(request.GET) > 0:
        if len(request.GET) != 1 or (not "op" in request.GET or request.GET["op"] != "crear"):
            return redirect("/cuentas")

    

    if request.method == "POST":
        if form.is_valid():
            user = request.user
            nombre = escape(form.cleaned_data.get("nombre_cuenta"))
            tipo = escape(form.cleaned_data.get("tipo_cuenta"))

            cuenta = Cuenta.objects.create(
                nombre=nombre,
                tipo=Cuenta.TipoCuenta(tipo),
                propietario=user,
            )

            cuenta.save()

            #OperationLog.objects.using('logsdb').create(
            #    user_id=user.id,
            #    user_username=user.username,
            #    operation="Nueva cuenta. ID: " + str(cuenta.id)
            #)

            return redirect("/cuentas")
        else:
            message = "No se pudo crear la cuenta"
       
    context = {
        "form": form,
        "cuentas": Cuenta.objects.filter(propietario=request.user),
        "seleccion": "cuenta",
        "op": op,
        "message": escape(message)
    }

    return render(request, "cuentas/cuentas.html", context=context)


@login_required
@require_http_methods(["GET", "POST"])
def movimiento_view(request):
    op = request.GET.get("op", "")
    user = request.user
    movimientos = Transaccion.objects.filter(origen__propietario__id=user.id)

    if len(request.GET) > 0:
        if len(request.GET) != 1 or (not "op" in request.GET or request.GET["op"] not in ["ingreso", "gasto", "traspaso"]):
            return redirect("/movimientos")

    form = None

    if op == "ingreso":
        cuentas_origen = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO)
        cuentas_destino = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO)
        form = MovimientoForm(cuentas_origen, cuentas_destino)

    elif op == "gasto":
        cuentas_origen = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO)
        cuentas_destino = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.GASTO)
        form = MovimientoForm(cuentas_origen, cuentas_destino)

    elif op == "traspaso":
        cuentas_origen = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO)
        cuentas_destino = Cuenta.objects.filter(tipo=Cuenta.TipoCuenta.INGRESO_EGRESO)
        form = MovimientoForm(cuentas_origen, cuentas_destino)

    if request.method == "POST":
        form = MovimientoForm(cuentas_origen, cuentas_destino, request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            origen_id = cleaned_data['cuenta_origen']
            destino_id = cleaned_data['cuenta_destino']
            cuenta_origen = Cuenta.objects.get(pk=origen_id)
            cuenta_destino = Cuenta.objects.get(pk=destino_id)
            transaccion = Transaccion.objects.create(
                origen=cuenta_origen,
                destino=cuenta_destino,
                fecha=cleaned_data['fecha'],
                monto=cleaned_data['monto'],
                concepto=cleaned_data['concepto']
            )
            transaccion.realizar()

            OperationLog.objects.using('logsdb').create(
                user_id=user.id,
                user_username=user.username,
                operation=f"Nueva transaccion. ID: {transaccion.id}"
            )

            movimientos = Transaccion.objects.filter(origen__propietario__id=user.id)
            return redirect("/movimientos")

    context = {
        "op": op,
        "movimientos": movimientos,
        "seleccion": "movimiento",
        "form": form
    }

    return render(request, "movimientos/movimientos.html", context=context)


