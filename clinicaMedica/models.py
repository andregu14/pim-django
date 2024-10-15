from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime

class FuncionarioManager(BaseUserManager):
    def create_user(self, email, cpf, nome, cargo, salario, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, nome=nome, cargo=cargo, salario=salario, **extra_fields)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, nome, cargo, salario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, cpf, nome, cargo, salario, password, **extra_fields)

class Funcionario(AbstractBaseUser, PermissionsMixin):
    SEXO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    ]
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True, blank=False)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    is_first_login = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name="Data de Ingresso", default=timezone.now)
    sexo = models.CharField(max_length=15, choices=SEXO_CHOICES, blank=False)

    objects = FuncionarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'nome', 'cargo', 'salario']

    def save(self, *args, **kwargs):
        if self.is_first_login and not self.password:
            self.set_password(None)
        super().save(*args, **kwargs)
    
    def first_name(self):
        return self.nome.split()[0]
    
    def first_two_names(self):
        parts = self.nome.split()
        if len(parts) == 1:
            name = self.nome
        elif len(parts) == 2:
            name = f"{parts[0]} {parts[1]}"
        else:
            name = f"{parts[0]} {parts[-1]}"
        
        # Verifica se o funcionário é um Dentista
        if hasattr(self, 'dentista'):
            if self.dentista.sexo == 'masculino':
                return f"Dr. {name}"
            else:
                return f"Dra. {name}"
        return name

    def __str__(self):
        return self.first_two_names()

class Dentista(Funcionario):
    PERIODO_CHOICES = [
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'),
        ('diurno', 'Diurno'),
    ]
    especializacao = models.CharField(max_length=60)
    periodo_trabalho = models.CharField(max_length=10, choices=PERIODO_CHOICES, default='diurno', blank=False)
    cro = models.CharField(max_length=20, blank=False, unique=True, verbose_name="CRO") # numero do registro do conselho regional de odontologia

    def get_horarios_disponiveis(self, data):
        horarios = []
        data_inicio = timezone.make_aware(datetime.combine(data, datetime.min.time()))
        data_fim = timezone.make_aware(datetime.combine(data, datetime.max.time()))
        
        if self.periodo_trabalho in ['matutino', 'diurno']:
            inicio = data_inicio.replace(hour=7, minute=0)
            fim = data_inicio.replace(hour=12, minute=0)
            horarios.extend(self._gerar_horarios(inicio, fim))
        
        if self.periodo_trabalho in ['vespertino', 'diurno']:
            inicio = data_inicio.replace(hour=12, minute=10)
            fim = data_inicio.replace(hour=19, minute=0)
            horarios.extend(self._gerar_horarios(inicio, fim))
        
        # Filtrar horários já agendados
        consultas_agendadas = Consulta.objects.filter(
            medico_dentista=self,
            data_hora__range=(data_inicio, data_fim)
        ).values_list('data_hora', flat=True)

        horarios_disponiveis = [
            h for h in horarios if h not in consultas_agendadas
        ]
        
        return horarios_disponiveis

    def _gerar_horarios(self, inicio, fim):
        horarios = []
        while inicio <= fim:
            horarios.append(inicio)
            inicio += timedelta(minutes=15)
        return horarios

class Recepcionista(Funcionario):
    pass

    def __str__(self):
        return self.nome

class Gestor(Funcionario):
    pass

    def __str__(self):
        return self.nome

class Paciente(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    telefone = models.CharField(max_length=50, blank=False)
    endereco = models.CharField(max_length=50, blank=False)
    data_de_nascimento = models.DateField(verbose_name="Data de Nascimento", blank=False)
    sexo = models.CharField(max_length=9, blank=False)
    estado = models.CharField(max_length=50, blank=False)
    cep = models.CharField(max_length=9, blank=True)
    date_joined = models.DateTimeField(verbose_name="Data do Cadastro", default=timezone.now)

    def calcular_idade(self):
        hoje = date.today()
        return hoje.year - self.data_de_nascimento.year - ((hoje.month, hoje.day) < (self.data_de_nascimento.month, self.data_de_nascimento.day))

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    data_hora = models.DateTimeField(verbose_name="Data e Hora", blank=False)
    status = models.CharField(max_length=20)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_dentista = models.ForeignKey(Dentista, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('data_hora', 'medico_dentista')

    def clean(self):
    # Verifica se já existe uma consulta para o mesmo dentista no mesmo horário
        if Consulta.objects.filter(medico_dentista=self.medico_dentista, data_hora=self.data_hora).exists():
            raise ValidationError("Já existe uma consulta agendada para este dentista neste horário.")

    def save(self, *args, **kwargs):
        self.full_clean()   
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Consulta {self.id} - {self.paciente.nome} com {self.medico_dentista.nome} em {localtime(self.data_hora).strftime('%d-%m-%Y %H:%M:%S')}"


class Servico(models.Model):
    nome = models.CharField(max_length=40, verbose_name="Serviço", blank=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome