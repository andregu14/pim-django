from django.shortcuts import render, redirect
from .models import Funcionario, Paciente
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import datetime

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito = 11 - (soma % 11)
    if digito > 9:
        digito = 0
    if int(cpf[9]) != digito:
        return False
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito = 11 - (soma % 11)
    if digito > 9:
        digito = 0
    if int(cpf[10]) != digito:
        return False
    
    return True

# Create your views here.
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        funcionario = authenticate(request, email=email, password=senha)
        if funcionario is not None:
            login(request, funcionario)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email ou senha incorretos', 'danger')
    return render(request, 'pages-login.html')

def primeiro_acesso(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        funcionario = None
        try:
            funcionario = Funcionario.objects.get(email=email)
        except Funcionario.DoesNotExist:
            messages.error(request, 'Funcionário não encontrado', 'danger')
            return render(request, 'primeiro-acesso.html')

        if funcionario:
            if funcionario.is_first_login:
                funcionario.password = make_password(senha)
                funcionario.is_first_login = False
                funcionario.save()
                messages.success(request, 'Senha salva com sucesso')
                return redirect('login')
            else:
                messages.warning(request, 'Não é o primeiro login')
        else:
            messages.error(request, 'Funcionário não encontrado', 'danger')

    return render(request, 'primeiro-acesso.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'index.html')

@login_required
def perfil(request):
    return render(request, 'users-profile.html')

@login_required
def procurar_paciente(request):
    return render(request, 'procurar-paciente.html')

@login_required
def cadastrar_paciente(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        estado = request.POST.get('estado')
        cep = request.POST.get('cep')
        data_de_nascimento_str = request.POST.get('data_de_nascimento')
        try:
            data_de_nascimento = datetime.strptime(data_de_nascimento_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Formato de data inválido. Use YYYY-MM-DD.', 'danger')
            return render(request, 'cadastrar-paciente.html')

        # Remove formatação do CPF
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        if not validar_cpf(cpf_limpo):
            messages.error(request, 'CPF inválido', 'danger')
            return render(request, 'cadastrar-paciente.html')    

        # Verifica se o cpf ou email já existem
        if Paciente.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado', 'danger')
            return render(request, 'cadastrar-paciente.html')
        if Paciente.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado', 'danger')
            return render(request, 'cadastrar-paciente.html')

        try:
            # Cria um novo paciente
            paciente = Paciente(
                cpf=cpf,    
                nome=nome,
                email=email,
                telefone=telefone,
                endereco=endereco,
                data_de_nascimento=data_de_nascimento,
                estado=estado,
                cep=cep
            )
            paciente.save()
            messages.success(request, 'Paciente cadastrado com sucesso')
        except IntegrityError:
            messages.error(request, 'Erro ao cadastrar paciente. Verifique os dados e tente novamente', 'danger')
            return render(request, 'cadastrar-paciente.html')
    return render(request, 'cadastrar-paciente.html')

@login_required
def funcionario(request):
    return render(request, 'pages.funcionario.html')

@login_required
def faq(request):
    return render(request, 'pages-faq.html')

@login_required
def contato(request):
    return render(request, 'pages-contact.html')