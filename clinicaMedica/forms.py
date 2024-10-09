from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Gestor, Dentista, Recepcionista

class RecepcionistaCreationForm(forms.ModelForm):
    class Meta:
        model = Recepcionista
        fields = ('email', 'nome', 'cpf', 'cargo', 'salario')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # Define uma senha inutilizável
        if commit:
            user.save()
        return user

class GestorCreationForm(forms.ModelForm):
    class Meta:
        model = Gestor
        fields = ('email', 'nome', 'cpf', 'cargo', 'salario')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # Define uma senha inutilizável
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

class DentistaCreationForm(forms.ModelForm):
    class Meta:
        model = Dentista
        fields = ('email', 'nome', 'cpf', 'cargo', 'especializacao', 'salario','periodo_trabalho')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # Define uma senha inutilizável
        if commit:
            user.save()
        return user