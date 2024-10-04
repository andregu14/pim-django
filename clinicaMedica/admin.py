from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RecepcionistaCreationForm, GestorCreationForm, DentistaCreationForm

from .models import Funcionario, Dentista, Recepcionista, Gestor, Paciente, Consulta


class FuncionarioAdmin(UserAdmin):
    model = Funcionario
    list_display = ('email', 'nome', 'cpf', 'cargo', 'date_joined')
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)
    fieldsets = (
        ('Autenticação', {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario')}),
    )

    list_filter = ('nome', 'cargo', 'date_joined')

    def has_add_permission(self, request):
        return False

class GestorAdmin(UserAdmin):
    add_form = GestorCreationForm
    model = Gestor
    list_display = ('email', 'nome', 'cpf', 'cargo', 'date_joined')
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)
    fieldsets = (
        ('Autenticação', {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario')}),
    )
    add_fieldsets = (
        ('Autenticação', {'fields': ('email',)}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario')}),
    )

    list_filter = ('nome', 'cargo', 'date_joined')

class DentistaAdmin(UserAdmin):
    add_form = DentistaCreationForm
    model = Dentista
    list_display = ('email', 'nome', 'cpf', 'cargo', 'especializacao', 'date_joined')
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)
    fieldsets = (
        ('Autenticação', {'fields': ('email',)}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario', 'especializacao')}),
    )
    add_fieldsets = (
        ('Autenticação', {'fields': ('email',)}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario', 'especializacao')}),
    )

    list_filter = ('nome', 'cargo', 'date_joined')

class RecepcionistaAdmin(UserAdmin):
    add_form = RecepcionistaCreationForm
    model = Recepcionista
    list_display = ('email', 'nome', 'cpf', 'cargo', 'date_joined')
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)
    fieldsets = (
        ('Autenticação', {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario')}),
    )
    add_fieldsets = (
        ('Autenticação', {'fields': ('email',)}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'cargo', 'salario')}),
    )
    
    list_filter = ('nome', 'cargo', 'date_joined')

admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Dentista, DentistaAdmin)
admin.site.register(Recepcionista, RecepcionistaAdmin)
admin.site.register(Gestor, GestorAdmin)
admin.site.register(Paciente)
admin.site.register(Consulta)