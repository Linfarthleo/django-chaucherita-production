from django import forms
from django.utils.html import escape

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

    def clean_tipo_cuenta(self):
        tipo_cuenta = self.cleaned_data['tipo_cuenta']
        choices = [choice[0] for choice in Cuenta.TipoCuenta.choices]
        if tipo_cuenta not in choices:
            raise forms.ValidationError('Tipo de cuenta no válido')
        return tipo_cuenta

    def clean(self):
        cleaned_data = super().clean()
        for field_name in cleaned_data:
            value = cleaned_data[field_name]
            if isinstance(value, str):  
                cleaned_data[field_name] = escape(value)
            if any(char in value for char in [';', '--', "'", '"', '#', '/*', '*/', '<script>', '<img>', '<svg>', '<', '>', '(', ')']):
                raise forms.ValidationError('Caracteres no permitidos en los campos')
        return cleaned_data


class MovimientoForm(forms.Form):
    
    def __init__(self, origen, destino, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        choices_origen = [(cuenta.id, cuenta.nombre) for cuenta in origen]
        self.fields['cuenta_origen'] = forms.ChoiceField(choices=choices_origen, label='Cuenta de origen')

        choices_destino = [(cuenta.id, cuenta.nombre) for cuenta in destino]
        self.fields['cuenta_destino'] = forms.ChoiceField(choices=choices_destino, label='Cuenta de destino')

    monto = forms.FloatField(label='Monto')
    concepto = forms.CharField(label='Concepto', widget=forms.Textarea)
    fecha = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'type': 'date'}))


    def clean_concepto(self):
        concepto = self.cleaned_data['concepto']
        if isinstance(concepto, str): 
            concepto = escape(concepto)
        if any([char in concepto for char in [';', '--', "'", '"', '#', '/*', '*/', '<script>', '<img>', '<svg>', '<', '>', '(', ')']]):
            raise forms.ValidationError('El concepto no puede contener caracteres especiales')
        return concepto

    def clean_monto(self):
        monto = self.cleaned_data['monto']
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise forms.ValidationError('El monto debe ser un número mayor que cero')
        return monto
