from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.contrib import messages
from .forms import FormLogin
from django.contrib.auth.decorators import login_required


def homepage(request):
    context= {}
    return render(request, 'homepage.html', context)

def login(request):
    context = {}
    dados_senai = Senai.objects.all()
    context["dados_senai"] = dados_senai

    if request.method == "POST":
        form = FormLogin(request.POST)
        if form.is_valid():
            var_username = form.cleaned_data['username']
            var_senha = form.cleaned_data['senha']

            # Autenticar usuário
            user = authenticate(username=var_username, password=var_senha)
            if user is not None:
                # Fazer login do usuário
                auth_login(request, user)
                # Redirecionar para a página de cursos após login bem-sucedido
                return redirect("cursos")
            else:
                # Adicionar mensagem de erro se as credenciais forem inválidas
                messages.error(request, "Nome de usuário ou senha incorretos")
                redirect("login")
    else:
        form = FormLogin()

    context.update({"form": form})
    return render(request, 'login.html', context)

@login_required
def cadastro(request):
    context = {}
    dados_senai = Senai.objects.all()
    context["dados_senai"] = dados_senai


    if request.method == "POST":
        form = FormCadastro(request.POST)
        if form.is_valid():
            var_nome = form.cleaned_data['nome']
            var_sobrenome = form.cleaned_data['sobrenome']
            var_username = form.cleaned_data['username']
            var_senha = form.cleaned_data['senha']

            try:
                user = User.objects.create_user(username=var_username, password=var_senha)
                user.first_name = var_nome
                user.last_name = var_sobrenome
                user.save()

                coordenacao_group = Group.objects.get(name='COORDENAÇÃO')
                user.groups.add(coordenacao_group)

                #Cria o perfil do usuário personalizado
                Usuario.objects.create(
                    nome=var_nome,
                    sobrenome=var_sobrenome,
                    username=var_username,
                    senha=var_senha,
                    cargo="COORDENAÇÃO",
                )
                messages.success(request, "Usuário cadastrado.")
                return redirect("cadastro")
            
            except IntegrityError:
                messages.error(request, "Nome de usuário já existe. Por favor, escolha outro nome de usuário.")
                #Renderizar o formulário com dados existentes
                context.update({"form": form})
                return render(request, 'cadastro.html', context)
        else:
            #Se o formulário não for válido, renderize a página com erros do formulário
            context.update({"form": form})
            return render(request, 'cadastro.html', context)
    else:
        form = FormCadastro()

    #Definindo as variáveis de permissão no contexto
    if request.user.is_authenticated:
        context['is_coordenacao'] = request.user.groups.filter(name='Coordenação').exists()
        context['is_administracao'] = request.user.groups.filter(name='Administração').exists()
    else:
        context['is_coordenacao'] = False
        context['is_administracao'] = False

    context.update({"form": form})
    return render(request, 'cadastro.html', context)

def cursos(request):
    return render(request, 'cursos.html')

def relatorio(request):
    return render(request, 'relatorio.html')

def alunos(request):
    return render(request, 'alunos.html')
