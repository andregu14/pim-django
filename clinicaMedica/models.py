from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils import timezone

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
    id_funcionario = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, blank=False)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    is_first_login = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name="Data de Ingresso", default=timezone.now)

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
            return self.nome
        elif len(parts) == 2:
            return f"{parts[0]} {parts[1]}"
        else:
            return f"{parts[0]} {parts[-1]}"

    def __str__(self):
        return self.nome

class Dentista(Funcionario):
    especializacao = models.CharField(max_length=60)

    def __str__(self):
        return self.nome

class Recepcionista(Funcionario):
    pass

    def __str__(self):
        return self.nome

class Gestor(Funcionario):
    pass

    def __str__(self):
        return self.nome

class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    telefone = models.CharField(max_length=50, blank=False)
    data_de_nascimento = models.DateField(verbose_name="Data de Nascimento", blank=False)

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField(verbose_name="Data e Hora", blank=False)
    status = models.CharField(max_length=20)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_dentista = models.ForeignKey(Dentista, on_delete=models.CASCADE)

    def __str__(self):
        return f"Consulta {self.id_consulta} - {self.paciente.nome} com {self.medico_dentista.nome} em {self.data_hora}"
