from django import forms

from cuentas.models import Cuenta


class CrearCuentaForm(forms.Form):
    nombre_cuenta = forms.CharField(label='Nombre de cuenta', max_length=30)
    tipo_cuenta = forms.ChoiceField(label='Tipo de cuenta', choices=Cuenta.TipoCuenta.choices)

    def clean_nombre_cuenta(self):
        nombre_cuenta = self.cleaned_data['nombre_cuenta']
        if len(nombre_cuenta) < 3:
            raise forms.ValidationError('El nombre de la cuenta debe tener al menos 3 caracteres')
        elif '<script>' in nombre_cuenta:
            raise forms.ValidationError('El nombre de la cuenta no puede contener scripts')
        return nombre_cuenta
