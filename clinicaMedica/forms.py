from django import forms
from .models import MedicoDentista
class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = MedicoDentista
        fields = ['cpf', 'email', 'salario', 'cargo', 'nome']
        exclude = ['senha']