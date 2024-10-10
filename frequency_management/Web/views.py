from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import csv
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

def homepage(request):
    return render(request, 'homepage.html')

def login(request):
    context = {}

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
                return redirect("cursos")
            else:
                # Adicionar mensagem de erro se as credenciais forem inválidas
                messages.error(request, "Nome de usuário ou senha incorretos.")
                return redirect("login")
    else:
        form = FormLogin()

    context.update({"form": form})
    return render(request, 'login.html', context)

@login_required
def cadastro(request):
    context = {}

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

                # Cria o perfil do usuário personalizado
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
                context.update({"form": form})
                return render(request, 'cadastro.html', context)
        else:
            context.update({"form": form})
            return render(request, 'cadastro.html', context)
    else:
        form = FormCadastro()

    context.update({"form": form})
    return render(request, 'cadastro.html', context)

@login_required
def cursos(request):
    cursos_list = Curso.objects.all()
    return render(request, 'cursos.html', {'cursos': cursos_list})


@login_required
def relatorio(request):
    return render(request, 'relatorio.html')

@login_required
def alunos(request):
    return render(request, 'alunos.html')

@login_required
def notificacoes(request):
    return render(request, 'notificacoes.html')

@login_required
def delete_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    alunos = curso.aluno_set.all()
    
    if request.method == 'POST':
        alunos.delete()
        curso.delete()
        
        messages.success(request, "Curso e alunos associados excluídos com sucesso.")
        return redirect('cursos')

    context = {'curso': curso, 'alunos': alunos}
    return render(request, 'alunos.html')

def delete_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)

    if request.method == 'POST':
        aluno.delete()

        messages.success(request, "Aluno excluído com sucesso.")
        return redirect('alunos')


@login_required
def logout(request):
    auth_logout(request)
    return redirect("homepage")


def nomeUsuario(request):
    usuario = Usuario.objects.get(username=request.user.username)
    return usuario.nome



def criar_cursos(request):
    if request.method == 'POST' and 'cursos' in request.FILES:
        csv_file = request.FILES['cursos']
        
    
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        

        with open(fs.path(filename), newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=';') 
            next(reader) 
            
           
            for row in reader:
                try:
                    
                    dias = [dia.strip() for dia in row[6].split(',')]  
                    
                    Curso.objects.create(
                        turma=row[0],
                        nome_curso=row[1],             
                        horario_entrada=row[2],       
                        horario_saida=row[3],          
                        responsavel=row[4],            
                        dias_funcionamento=dias        
                    )
                except IndexError:
                    print(f"Linha mal formatada, ignorando: {row}")

        # Mensagem de sucesso ou redirecionamento
        messages.success(request, "Cursos criados com sucesso.")
        return redirect("cursos")
    
    return render(request, 'criar_curso.html')

def criar_alunos(request):
    if request.method == 'POST' and 'alunos' in request.FILES:
        csv_file = request.FILES['alunos']
        
 
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        
      
        with open(fs.path(filename), newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=';') 
            next(reader)  
            
           
            for row in reader:
                try:
                    
                    curso_id = row[2].strip()  
                    curso = Curso.objects.get(turma=curso_id) 
                    
                    
                    Aluno.objects.create(
                        nome=row[0].strip(),  
                        id_carteirinha=int(row[1].strip()),  
                        id_curso=curso  
                    )
                except IndexError:
                    print(f"Linha mal formatada, ignorando: {row}")
                except Curso.DoesNotExist:
                    print(f"Curso com turma '{curso_id}' não encontrado, ignorando: {row}")
                except ValueError:
                    print(f"Erro ao converter id_carteirinha para inteiro: {row[1].strip()}")
                except Exception as e:
                    print(f"Erro ao criar aluno: {e}, ignorando linha: {row}")

        messages.success(request, "Alunos criados com sucesso.")
        return redirect("alunos")
    
    return render(request, 'criar_aluno.html')
