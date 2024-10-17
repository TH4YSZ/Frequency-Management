from .models import *
from .forms import *
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Count
from django.db import IntegrityError
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
import csv

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
    cursos = Curso.objects.all()
    return render(request, 'cursos.html', {'cursos': cursos})


@login_required
def relatorio(request):
    return render(request, 'relatorio.html')

@login_required
def alunos(request, turma):
    curso = get_object_or_404(Curso, turma=turma)
    alunos = Aluno.objects.filter(id_curso=curso)
    
    def processar_frequencia_aluno(aluno):
        # Frequências entre a data de início e a data ajustada (descontando 30 dias do fim)
        frequencias = Frequencia.objects.filter(
            id_aluno=aluno, 
            data__range=[curso.data_inicio, curso.data_fim - timedelta(days=30)]
        )
        
        # Contagem de dias letivos baseados nos dias de funcionamento do curso
        dias_funcionamento = set(curso.dias_funcionamento)  # Ex: ['SEG', 'TER', 'QUA']
        data_atual = curso.data_inicio
        dias_letivos = 0

        # Iteramos pelos dias do curso, considerando as datas de início e fim ajustadas
        while data_atual <= curso.data_fim - timedelta(days=30):
            # Obtém o nome do dia da semana em português (ex: 'SEG', 'TER', etc.)
            nome_dia_semana = data_atual.strftime('%a').upper()[:3]  # Abreviação do dia da semana em PT-BR
            if nome_dia_semana in dias_funcionamento:
                dias_letivos += 1
            data_atual += timedelta(days=1)

        # Inicializando variáveis
        faltas = 0
        atrasos = 0
        carga_aluno = 0
        
        # Processando as frequências
        for dia in range(dias_letivos):
            registros_dia = frequencias.filter(data=data_atual)
            registro_entrada = registros_dia.filter(identificador=1).first()
            registro_saida = registros_dia.filter(identificador=2).last()

            # Contagem de faltas
            if not registro_entrada:  # Se não há registro de entrada no dia letivo
                faltas += 1
            else:
                # Verificando se há atraso
                if registro_entrada.hora > curso.horario_entrada:
                    atrasos += 1
                
                # Contagem de carga horária
                if registro_saida:
                    # Se o aluno saiu antes do horário de saída do curso
                    if registro_saida.hora < curso.horario_saida:
                        # Calculando quanto tempo o aluno ficou
                        tempo_frequentado = (registro_saida.hora - registro_entrada.hora).total_seconds() / 3600
                        
                        # Descontando da carga horária total (1200h)
                        carga_aluno += tempo_frequentado
                    else:
                        # Se o aluno saiu após o horário de saída do curso ou exatamente na hora
                        tempo_maximo = (curso.horario_saida - registro_entrada.hora).total_seconds() / 3600
                        carga_aluno += tempo_maximo

        # Cálculo da porcentagem da carga horária cumprida
        porcentagem_carga_horaria = (carga_aluno / curso.carga_horaria) * 100

        return {
            'faltas': faltas,
            'atrasos': atrasos,
            'carga_horaria_aluno': carga_aluno,
            'porcentagem_carga_horaria': porcentagem_carga_horaria
        }

    # Processando a frequência para cada aluno
    alunos_detalhes = []
    for aluno in alunos:
        detalhes_aluno = processar_frequencia_aluno(aluno)
        alunos_detalhes.append({
            'aluno': aluno,
            'faltas': detalhes_aluno['faltas'],
            'atrasos': detalhes_aluno['atrasos'],
            'carga_horaria_aluno': detalhes_aluno['carga_horaria_aluno'],
            'porcentagem_carga_horaria': detalhes_aluno['porcentagem_carga_horaria']
        })

    context = {
        'curso': curso,
        'alunos_detalhes': alunos_detalhes  # Enviamos a lista de alunos com detalhes
    }

    return render(request, 'alunos.html', context)

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
 
            
            for row in reader:
                try:

                    dias = [dia.strip() for dia in row[6].split(',')]  
                    

                    data_inicio = datetime.strptime(row[7], '%d/%m/%Y').date()
                    data_fim = datetime.strptime(row[8], '%d/%m/%Y').date()

                    Curso.objects.create(
                        turma=row[0],                     
                        nome_curso=row[1],                
                        horario_entrada=row[2],            
                        horario_saida=row[3],
                        carga_horaria=row[4],             
                        responsavel=row[5],                
                        dias_funcionamento=dias,          
                        data_inicio=data_inicio,           
                        data_fim=data_fim                  
                    )
                except (IndexError, ValueError) as e:
    
                    print(f"Linha mal formatada ou erro: {row}, Erro: {e}")

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
                    messages.error(request, "Erro ao criar alunos.")

        messages.success(request, "Alunos criados com sucesso.")
        return redirect("cursos")   
    
    return render(request, 'criar_aluno.html')

def processar_frequencia_aluno(aluno):
    curso = aluno.id_curso
    frequencias = Frequencia.objects.filter(id_aluno=aluno, data__range=[curso.data_inicio, curso.data_fim])
    
    # Calculando dias letivos com base nos dias de funcionamento do curso
    dias_funcionamento = set(curso.dias_funcionamento)
    data_atual = curso.data_inicio
    dias_letivos = 0

    while data_atual <= curso.data_fim:
        if data_atual.strftime('%a') in dias_funcionamento:
            dias_letivos += 1
        data_atual += timedelta(days=1)

    # Inicializando variáveis
    faltas = 0
    atrasos = 0
    carga_aluno = 0
    
    # Processando as frequências
    for dia in range(dias_letivos):
        registros_dia = frequencias.filter(data=data_atual)
        registro_entrada = registros_dia.filter(identificador=1).first()
        registro_saida = registros_dia.filter(identificador=2).last()

        # Contagem de faltas
        if not registro_entrada:  # Se não há registro de entrada no dia letivo
            faltas += 1
        else:
            # Verificando se há atraso
            if registro_entrada.hora > curso.horario_entrada:
                atrasos += 1
            
            # Contagem de carga horária
            if registro_saida:
                # Se saiu antes da hora de saída do curso
                if registro_saida.hora <= curso.horario_saida:
                    carga_aluno += (registro_saida.hora - registro_entrada.hora).total_seconds() / 3600  # Convertendo segundos para horas
                else:
                    # Se saiu após o horário de saída, conta o horário do curso
                    carga_aluno += (curso.horario_saida - registro_entrada.hora).total_seconds() / 3600

    # Cálculo da porcentagem da carga horária cumprida
    porcentagem_carga_horaria = (carga_aluno / curso.carga_horaria) * 100

    return {
        'faltas': faltas,
        'atrasos': atrasos,
        'carga_horaria_aluno': carga_aluno,
        'porcentagem_carga_horaria': porcentagem_carga_horaria
    }