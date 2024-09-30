from django.contrib import admin
from .forms import FuncionarioForm

from .models import MedicoDentista, Recepcionista, Gestor, Paciente, Consulta


class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('id_consulta', 'data_hora', 'status', 'paciente_id', 'medico_dentista_id')
    search_fields = ('paciente__nome', 'medico_dentista__nome', 'status')

class FuncionarioAdmin(admin.ModelAdmin):
    form = FuncionarioForm
    add_form = FuncionarioForm
    list_display = ('nome', 'cpf', 'email', 'cargo', 'salario')
    search_fields = ('nome', 'cpf', 'email')

# Register your models here.

admin.site.register(MedicoDentista, FuncionarioAdmin)
admin.site.register(Recepcionista, FuncionarioAdmin)
admin.site.register(Gestor, FuncionarioAdmin)
admin.site.register(Paciente)
admin.site.register(Consulta, ConsultaAdmin)
