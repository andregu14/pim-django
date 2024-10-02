from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import FuncionarioCreationForm

from .models import Funcionario, MedicoDentista, Recepcionista, Gestor, Paciente, Consulta


class FuncionarioAdmin(UserAdmin):
    add_form = FuncionarioCreationForm
    model = Funcionario
    list_display = ('email', 'nome', 'cpf', 'cargo', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario')}),
        ('Permissões', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cpf', 'cargo', 'salario', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    list_filter = ('is_staff', 'is_superuser')

class GestorAdmin(UserAdmin):
    add_form = FuncionarioCreationForm
    model = Gestor
    list_display = ('email', 'nome', 'cpf', 'cargo', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario')}),
        ('Permissões', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cpf', 'cargo', 'salario', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    list_filter = ('is_staff', 'is_superuser')

admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(MedicoDentista)
admin.site.register(Recepcionista)
admin.site.register(Gestor, GestorAdmin)
admin.site.register(Paciente)
admin.site.register(Consulta)
