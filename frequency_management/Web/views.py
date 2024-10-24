from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import IntegrityError
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import csv
from django.db import connection


from django.db import connection


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
    search_query = request.GET.get('search', '')

    if search_query:
        cursos = Curso.objects.filter(
            nome_curso__icontains=search_query
        ) | Curso.objects.filter(
            turma__icontains=search_query
        )
    else:
        cursos = Curso.objects.all()

    form = FormPesquisa(initial={'search': search_query})

    return render(request, 'cursos.html', {'form': form, 'cursos': cursos})


@login_required
def relatorio(request):
    
    return render(request, 'relatorio.html')



@login_required
def alunos(request, turma):
    curso = get_object_or_404(Curso, turma=turma)

    with connection.cursor() as cursor:
        cursor.execute("""
            WITH frequencias_calculadas AS (
                SELECT 
                    f.id_aluno_id,
                    f.data,
                    f.hora,
                    LEAD(f.hora) OVER (PARTITION BY f.id_aluno_id ORDER BY f.data, f.hora) AS proxima_hora,
                    CAST(f.identificador AS INTEGER) AS identificador
                FROM 
                    web_frequencia AS f
            ),
            dias_letivos AS (
                SELECT 
                    aluno.id_carteirinha,
                    COUNT(DISTINCT CASE WHEN CAST(f.identificador AS INTEGER) = 1 AND f.hora IS NULL THEN f.data END) AS total_faltas,
                    COUNT(DISTINCT CASE WHEN CAST(f.identificador AS INTEGER) = 1 AND (f.hora IS NULL OR f.hora > c.horario_entrada) THEN f.data END) AS total_atrasos,
                    SUM(
                        CASE 
                            WHEN CAST(f.identificador AS INTEGER) = 1 THEN 
                                GREATEST(0, 
                                    LEAST(
                                        EXTRACT(EPOCH FROM (COALESCE(f.proxima_hora, c.horario_saida) - COALESCE(f.hora, c.horario_entrada))) / 3600, 
                                        EXTRACT(EPOCH FROM (c.horario_saida - c.horario_entrada)) / 3600
                                    ) 
                                    - CASE WHEN COALESCE(f.hora, c.horario_entrada) < c.horario_entrada THEN 
                                        EXTRACT(EPOCH FROM (c.horario_entrada - COALESCE(f.hora, c.horario_entrada))) / 3600
                                    ELSE 0
                                    END
                                )
                            ELSE 0
                        END
                    ) AS carga_horaria_total
                FROM 
                    web_aluno AS aluno
                LEFT JOIN 
                    frequencias_calculadas AS f ON aluno.id_carteirinha = f.id_aluno_id
                JOIN 
                    web_curso AS c ON aluno.id_curso_id = c.turma
                WHERE 
                    c.turma = %s
                    AND f.data BETWEEN c.data_inicio AND c.data_fim
                GROUP BY 
                    aluno.id_carteirinha
            )
            SELECT 
                aluno.nome,
                dl.total_faltas,
                dl.total_atrasos,
                dl.carga_horaria_total,
                CASE 
                    WHEN c.carga_horaria > 0 THEN 
                        LEAST(100, (dl.carga_horaria_total / c.carga_horaria) * 100)
                    ELSE 0
                END AS porcentagem_carga_horaria
            FROM 
                dias_letivos AS dl
            JOIN 
                web_aluno AS aluno ON dl.id_carteirinha = aluno.id_carteirinha
            JOIN 
                web_curso AS c ON aluno.id_curso_id = c.turma
            WHERE 
                c.turma = %s
        """, [curso.turma, curso.turma])

        resultados = cursor.fetchall()

    if not resultados:
        alunos_detalhes = []
    else:
        alunos_detalhes = []
        for resultado in resultados:
            alunos_detalhes.append({
                'aluno': resultado[0],
                'faltas': resultado[1],
                'atrasos': resultado[2],
                'carga_horaria_aluno': resultado[3],
                'porcentagem_carga_horaria': round(resultado[4], 2),  
            })

    context = {
        'curso': curso,
        'alunos_detalhes': alunos_detalhes,
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

def upload_frequencia(request):
    if request.method == 'POST' and 'freq' in request.FILES:
        txt_file = request.FILES['freq']

        fs = FileSystemStorage()
        filename = fs.save(txt_file.name, txt_file)

        # Abrir o arquivo TXT
        with open(fs.path(filename), newline='', encoding='ISO-8859-1') as txtfile:
            reader = csv.reader(txtfile, delimiter='\t')  # Usando tabulação como delimitador

            for row in reader:
                try:
                    # Assumindo que o TXT contém as colunas na ordem: data, id_carteirinha, hora, identificador
                    data = row[0].strip()  # Data da frequência
                    id_carteirinha = int(row[1].strip())
                    hora = row[2].strip()  # Hora da frequência
                    identificador = int(row[3].strip())  # Identificador de entrada ou saída

                    # Buscar o aluno pelo id_carteirinha
                    aluno = Aluno.objects.get(id_carteirinha=id_carteirinha)

                    # Criar a frequência no banco
                    Frequencia.objects.create(
                        id_aluno=aluno,
                        data=data,
                        hora=hora,
                        identificador=identificador
                    )

                except Aluno.DoesNotExist:
                    messages.error(request, f"Aluno com carteirinha {id_carteirinha} não encontrado.")
                except IndexError:
                    messages.error(request, "Erro no formato do arquivo TXT.")
                except Exception as e:
                    messages.error(request, f"Erro ao salvar a frequência: {str(e)}")

        messages.success(request, "Frequências carregadas com sucesso.")
        return redirect("homepage")

    return render(request, 'frequencia.html')
