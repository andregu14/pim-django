from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Funcionario, Gestor, MedicoDentista

class FuncionarioCreationForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('email', 'nome', 'cpf', 'cargo', 'salario', 'is_staff', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # Define uma senha inutilizável
        if commit:
            user.save()
        return user

class GestorCreationForm(forms.ModelForm):
    class Meta:
        model = Gestor
        fields = ('email', 'nome', 'cpf', 'cargo', 'salario', 'is_staff', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # Define uma senha inutilizável
        if commit:
            user.save()
        return user

class DentistaCreationForm(forms.ModelForm):
    class Meta:
        model = MedicoDentista
        fields = ('email', 'nome', 'cpf', 'cargo', 'especializacao', 'salario', 'is_staff', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # Define uma senha inutilizável
        if commit:
            user.save()
        return user