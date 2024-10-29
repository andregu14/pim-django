"""
URL configuration for pim project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clinicaMedica import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('admin/', admin.site.urls, name='admin'),
    path("login/", views.funcionario_login, name='login'),
    path('primeiro-acesso/', views.primeiro_acesso, name='primeiro_acesso'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('procurar-paciente/', views.procurar_paciente, name='procurar-paciente'),
    path('cadastrar-paciente/', views.cadastrar_paciente, name='cadastrar-paciente'),
    path('funcionario/', views.funcionario, name='funcionario'),
    path('faq/', views.faq, name='faq'),
    path('contato/', views.contato, name='contato'),
    path('marcar-consultas/', views.marcar_consultas, name='marcar-consultas'),
    path('get-datas-disponiveis/', views.get_datas_disponiveis, name='get_datas_disponiveis'),
    path('get-horarios-disponiveis/', views.get_horarios_disponiveis, name='get_horarios_disponiveis'),
    path('verificar-paciente/', views.verificar_paciente, name='verificar_paciente'),
    path('visualizar-consultas/', views.visualizar_consultas, name='visualizar_consultas'),
]
