from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, blank=False)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    senha = models.CharField(max_length=128, null=True, blank=True)
    is_first_login = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.senha and not self.senha.startswith('pbkdf2_sha256$'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    
    class Meta:
        abstract = True

class MedicoDentista(Funcionario):
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
    medico_dentista = models.ForeignKey(MedicoDentista, on_delete=models.CASCADE)

    def __str__(self):
        return f"Consulta {self.id_consulta} - {self.paciente.nome} com {self.medico_dentista.nome} em {self.data_hora}"

