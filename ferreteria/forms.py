from django import forms
from .models import Producto, ConsultaCliente

class ConsultaClienteForm(forms.ModelForm):
    class Meta:
        model = ConsultaCliente
        fields = ['nombre', 'correo', 'telefono', 'asunto', 'producto_interes', 'mensaje']
        
    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje')
        if len(mensaje) < 20:
            raise forms.ValidationError("El mensaje es muy corto. Debe tener al menos 20 caracteres.")
        return mensaje