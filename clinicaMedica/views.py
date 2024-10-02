from django.shortcuts import render, redirect
from .models import MedicoDentista, Recepcionista, Gestor
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
            funcionario = MedicoDentista.objects.get(email=email)
        except MedicoDentista.DoesNotExist:
            try:
                funcionario = Recepcionista.objects.get(email=email)
            except Recepcionista.DoesNotExist:
                try:
                    funcionario = Gestor.objects.get(email=email)
                except Gestor.DoesNotExist:
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
    return render(request, 'cadastrar-paciente.html')

@login_required
def funcionario(request):
    return render(request, 'pages.funcionario.html')

@login_required
def faq(request):
    return render(request, 'pages-faq.html')