from django.shortcuts import render, redirect
from .models import MedicoDentista, Recepcionista, Gestor
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        funcionario = authenticate(request, username=email, password=senha)
        if funcionario is not None:
            login(request, funcionario)
            print("Usuario autenticado")
            return redirect('home')
        else:
            print("Email ou senha incorretos")
            messages.error(request, 'Email ou senha incorretos')
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
                funcionario.senha = make_password(senha)
                funcionario.is_first_login = False
                funcionario.save()
                messages.success(request, 'Senha salva com sucesso')
                return redirect('login')
            else:
                messages.warning(request, 'Não é o primeiro login')
        else:
            messages.error(request, 'Funcionário não encontrado', 'danger')

    return render(request, 'primeiro-acesso.html')


