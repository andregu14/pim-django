from django.shortcuts import render, redirect
from .models import Funcionario, Paciente, Dentista, Consulta, Servico
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError

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
def funcionario_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        funcionario = authenticate(request, email=email, password=senha)
        if funcionario is not None:
            login(request, funcionario)
            return redirect('dashboard')
        else:
            try:
                primeiro_acesso = Funcionario.objects.get(email=email)
                if primeiro_acesso.is_first_login:
                    messages.warning(request, 'Primeiro login, cadastre sua senha')
                else:
                    messages.error(request, 'Email ou senha incorretos', 'danger')
            except Funcionario.DoesNotExist:    
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
    query = request.GET.get('procurar')
    if query:
        lista_de_pacientes = Paciente.objects.filter(
            nome__icontains=query
            ).union(
                Paciente.objects.filter(cpf__icontains=query)
            ).order_by('-id')
    else:
        lista_de_pacientes = Paciente.objects.all().order_by('-id')  # Ordena os pacientes pelo id em ordem decrescente
        
    paginator = Paginator(lista_de_pacientes, 12)  # Mostra até 12 pacientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'procurar-paciente.html', {'page_obj': page_obj, 'query':query})

@login_required
def cadastrar_paciente(request):
    if request.method == 'POST':    
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        sexo = request.POST.get('sexo')
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
                sexo=sexo,
                estado=estado,
                cep=cep
            )
            paciente.save()
            messages.success(request, 'Paciente cadastrado com sucesso')
        except:
            pass
    return render(request, 'cadastrar-paciente.html')

@login_required
def funcionario(request):
    query = request.GET.get('procurar')
    if query:
        lista_de_funcionarios = Funcionario.objects.filter(
            nome__icontains=query
            ).union(
                Funcionario.objects.filter(cpf__icontains=query)
            ).order_by('-id')
    else:
        lista_de_funcionarios = Funcionario.objects.all().order_by('-id')  # Ordena os pacientes pelo id em ordem decrescente

    paginator = Paginator(lista_de_funcionarios, 10)  # Mostra 10 até funcionarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages.funcionario.html', {'page_obj': page_obj, 'query':query})

@login_required
def faq(request):
    return render(request, 'pages-faq.html')

@login_required
def contato(request):
    return render(request, 'pages-contact.html')

@login_required
def marcar_consultas(request):
    if request.method == 'POST':
        dentista_id = request.POST.get('dentista')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        paciente_cpf = request.POST.get('paciente_cpf')
        servico_id = request.POST.get('servico')

        try:
            dentista = Dentista.objects.get(id=dentista_id)
            paciente = Paciente.objects.get(cpf=paciente_cpf)
            servico = Servico.objects.get(id=servico_id)
            
            # Combinar data e hora e adicionar informação de fuso horário
            data_hora_str = f"{data} {hora}"
            data_hora_naive = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M")
            data_hora = timezone.make_aware(data_hora_naive)

            print(data_hora)

            consulta = Consulta(
                data_hora=data_hora,
                status='agendada',
                paciente=paciente,
                medico_dentista=dentista,
                servico=servico,
            )
            consulta.save()
            messages.success(request, 'Consulta agendada com sucesso!')

        except ValidationError as e:
            messages.error(request, 'Erro ao agendar consulta', 'danger')
        except Exception as e:
            messages.error(request, 'Erro ao agendar consulta', 'danger')

    dentistas = Dentista.objects.all()
    servicos = Servico.objects.all()
    return render(request, 'marcar-consultas.html', {'dentistas': dentistas, 'servicos': servicos})

@login_required
def get_datas_disponiveis(request):
    dentista_id = request.GET.get('dentista_id')
    dentista = Dentista.objects.get(id=dentista_id)
    
    datas_disponiveis = []
    data_atual = datetime.now().date() + timedelta(days=1) # pega a data atual e adiciona um dia usando timedelta
    
    for i in range(15):
        data = data_atual + timedelta(days=i)
        if dentista.get_horarios_disponiveis(data):
            datas_disponiveis.append(data.strftime("%Y-%m-%d"))
    
    return JsonResponse({'datas': datas_disponiveis})

@login_required
def get_horarios_disponiveis(request):
    dentista_id = request.GET.get('dentista_id')
    data = request.GET.get('data')
    
    dentista = Dentista.objects.get(id=dentista_id)
    data_obj = datetime.strptime(data, "%Y-%m-%d").date()
    
    horarios_disponiveis = [h.strftime("%H:%M") for h in dentista.get_horarios_disponiveis(data_obj)]
    
    return JsonResponse({'horarios': horarios_disponiveis})

@login_required
def verificar_paciente(request):
    cpf = request.GET.get('cpf')
    try:
        paciente = Paciente.objects.get(cpf=cpf)
        return JsonResponse({'status': 'success', 'nome': paciente.nome})
    except Paciente.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Paciente não encontrado'})

@login_required
def teste(request):
        return render(request, 'teste-calendario.html')