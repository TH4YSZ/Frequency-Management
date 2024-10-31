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
from django.db import connection
from django.db import connection
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from io import BytesIO
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

            user = authenticate(username=var_username, password=var_senha)
            if user is not None:
                auth_login(request, user)
                return redirect("cursos")
            else:
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
def alunos(request, turma):
    curso = get_object_or_404(Curso, turma=turma)

    with connection.cursor() as cursor:
        cursor.execute("""
            WITH frequencias_calculadas AS (
                SELECT 
                    f.id_aluno_id,
                    f.data,
                    f.hora,
                    LEAD(f.hora) OVER (PARTITION BY f.id_aluno_id, f.data ORDER BY f.hora) AS proxima_hora,
                    CAST(f.identificador AS INTEGER) AS identificador,
                    CASE 
                        WHEN CAST(f.identificador AS INTEGER) = 2 
                        AND NOT EXISTS (
                            SELECT 1
                            FROM web_frequencia f2 
                            WHERE f2.id_aluno_id = f.id_aluno_id 
                            AND f2.data = f.data 
                            AND CAST(f2.identificador AS INTEGER) = 1
                        ) THEN true
                        ELSE false
                    END as apenas_saida
                FROM 
                    web_frequencia AS f
            ),
            presenca_por_dia AS (
                SELECT 
                    aluno.id_carteirinha,
                    f.data,
                    CASE 
                        WHEN f.apenas_saida THEN
                            EXTRACT(EPOCH FROM (
                                f.hora - c.horario_entrada
                            )) / 3600.0
                            - 
                            EXTRACT(EPOCH FROM c.carga_horaria_intervalo) / 3600.0
                        WHEN CAST(COALESCE(f.identificador, 0) AS INTEGER) = 1 THEN
                            CASE 
                                WHEN f.hora IS NULL THEN 0
                                ELSE
                                    EXTRACT(EPOCH FROM LEAST(
                                        COALESCE(f.proxima_hora, c.horario_saida),
                                        c.horario_saida
                                    ) - 
                                    GREATEST(
                                        f.hora,
                                        c.horario_entrada
                                    )) / 3600.0
                                    - 
                                    EXTRACT(EPOCH FROM c.carga_horaria_intervalo) / 3600.0
                            END
                        ELSE 0
                    END AS horas_presenca,
                    CASE 
                        WHEN f.id_aluno_id IS NULL THEN 1
                        WHEN f.apenas_saida THEN 0         
                        WHEN f.hora IS NULL AND CAST(COALESCE(f.identificador, 0) AS INTEGER) = 1 THEN 1 
                        ELSE 0 
                    END AS teve_falta,
                    CASE 
                        WHEN f.apenas_saida THEN 0
                        WHEN f.hora > c.horario_entrada + INTERVAL '10 minutes' AND CAST(COALESCE(f.identificador, 0) AS INTEGER) = 1 THEN 1 
                        ELSE 0 
                    END AS teve_atraso
                FROM 
                    web_aluno AS aluno
                CROSS JOIN
                    web_curso AS c 
                LEFT JOIN 
                    frequencias_calculadas AS f ON aluno.id_carteirinha = f.id_aluno_id
                    AND f.data BETWEEN c.data_inicio AND c.data_fim
                WHERE 
                    c.turma = %s
            ),
            totais_aluno AS (
                SELECT 
                    aluno.id_carteirinha,
                    COALESCE(SUM(p.horas_presenca), 0) AS total_horas_presenca,
                    COALESCE(COUNT(DISTINCT CASE WHEN p.teve_falta = 1 THEN p.data END), 0) AS total_faltas,
                    COALESCE(COUNT(DISTINCT CASE WHEN p.teve_atraso = 1 THEN p.data END), 0) AS total_atrasos
                FROM 
                    web_aluno AS aluno
                LEFT JOIN 
                    presenca_por_dia AS p ON aluno.id_carteirinha = p.id_carteirinha
                WHERE
                    aluno.id_curso_id = %s
                GROUP BY 
                    aluno.id_carteirinha
            )
            SELECT 
                aluno.id_carteirinha,
                aluno.nome,
                t.total_faltas,
                t.total_atrasos,
                LEAST(t.total_horas_presenca, 600) AS carga_horaria_cumprida,
                CASE 
                    WHEN c.dias_letivos > 0 THEN 
                        LEAST(100, ROUND((LEAST(t.total_horas_presenca, 600) / (c.dias_letivos * 7.5)) * 100, 2))
                    ELSE 0
                END AS porcentagem_frequencia
            FROM 
                web_aluno AS aluno
            JOIN 
                totais_aluno AS t ON aluno.id_carteirinha = t.id_carteirinha
            JOIN 
                web_curso AS c ON aluno.id_curso_id = c.turma
            WHERE 
                c.turma = %s
            ORDER BY 
                aluno.nome;
        """, [curso.turma, curso.turma, curso.turma])

        resultados = cursor.fetchall()

    alunos_detalhes = []
    for resultado in resultados:
        alunos_detalhes.append({
            'id_carteirinha': resultado[0],  # ou pode armazenar diretamente o ID aqui
            'aluno': resultado[1],
            'faltas': resultado[2],
            'atrasos': resultado[3],
            'carga_horaria_aluno': resultado[4],
            'porcentagem_carga_horaria': round(resultado[5], 2),
        })

    context = {
        'curso': curso,
        'alunos_detalhes': alunos_detalhes,
    }

    return render(request, 'alunos.html', context)




@login_required
def notificacoes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH frequencias_calculadas AS (
                SELECT 
                    f.id_aluno_id,
                    f.data,
                    f.hora,
                    LEAD(f.hora) OVER (PARTITION BY f.id_aluno_id, f.data ORDER BY f.hora) AS proxima_hora,
                    CAST(f.identificador AS INTEGER) AS identificador,
                    CASE 
                        WHEN CAST(f.identificador AS INTEGER) = 2 
                        AND NOT EXISTS (
                            SELECT 1
                            FROM web_frequencia f2 
                            WHERE f2.id_aluno_id = f.id_aluno_id 
                            AND f2.data = f.data 
                            AND CAST(f2.identificador AS INTEGER) = 1
                        ) THEN true
                        ELSE false
                    END as apenas_saida
                FROM 
                    web_frequencia AS f
            ),
            atrasos_aluno AS (
                SELECT 
                    aluno.id_carteirinha,
                    aluno.nome,
                    c.turma,
                    COUNT(DISTINCT CASE WHEN f.hora > c.horario_entrada + INTERVAL '10 minutes' AND CAST(COALESCE(f.identificador, 0) AS INTEGER) = 1 THEN f.data END) AS total_atrasos
                FROM 
                    web_aluno AS aluno
                JOIN 
                    web_curso AS c ON aluno.id_curso_id = c.turma
                LEFT JOIN 
                    frequencias_calculadas AS f ON aluno.id_carteirinha = f.id_aluno_id
                    AND f.data BETWEEN c.data_inicio AND c.data_fim
                GROUP BY 
                    aluno.id_carteirinha, aluno.nome, c.turma
                HAVING 
                    COUNT(DISTINCT CASE WHEN f.hora > c.horario_entrada + INTERVAL '10 minutes' AND CAST(COALESCE(f.identificador, 0) AS INTEGER) = 1 THEN f.data END) >= 3
            )
            SELECT 
                nome,
                turma,
                total_atrasos
            FROM 
                atrasos_aluno
            ORDER BY 
                nome;
        """)

        notificacoes = cursor.fetchall()

    alunos_notificados = []
    for notificacao in notificacoes:
        alunos_notificados.append({
            'nome': notificacao[0],
            'turma': notificacao[1],
            'total_atrasos': notificacao[2],
        })

    context = {
        'alunos_notificados': alunos_notificados,
    }

    return render(request, 'notificacoes.html', context)




@login_required
def delete_curso(request, turma):
    curso = get_object_or_404(Curso, turma=turma) 
    alunos = curso.aluno_set.all()  

    if request.method == 'POST':
        Frequencia.objects.filter(id_aluno__in=alunos).delete()
        alunos.delete()
        curso.delete()

        messages.success(request, "Curso e alunos associados excluídos com sucesso.")
        return redirect('cursos')

    context = {'curso': curso, 'alunos': alunos}
    return render(request, 'alunos.html', context)


@login_required
def delete_aluno(request, turma, id_carteirinha):
    curso = get_object_or_404(Curso, turma=turma)
    aluno = get_object_or_404(Aluno, id_carteirinha=id_carteirinha)
    
    if request.method == 'POST':
        
        # Depois exclui o aluno
        aluno.delete()
        
        print('aluno excluido')
        return redirect('cursos')  # Redireciona após a exclusão
    
    # Renderiza a página de confirmação de exclusão
    context = {
        'curso': curso,
        'aluno': aluno,
    }

    return render(request, 'alunos.html', context)


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
                        data_fim=data_fim,
                        carga_horaria_intervalo=row[9],
                        dias_letivos=row[10]
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
                    nome = row[0].strip()
                    
                    # Verifica se id_carteirinha não está vazio e é um número
                    if row[1].strip().isdigit():
                        id_carteirinha = int(row[1].strip())
                    else:
                        print(f"ID da carteirinha inválido para o aluno '{nome}'. Verifique o arquivo CSV.")
                        continue  # Pula para o próximo registro se o id_carteirinha estiver inválido

                    curso_id = row[2].strip()
                    
                    # Verifica se o curso existe
                    try:
                        curso = Curso.objects.get(turma=curso_id)
                    except Curso.DoesNotExist:
                        print(f"Curso com turma '{curso_id}' não encontrado para o aluno '{nome}'. Verifique o arquivo CSV.")
                        continue  # Pula este registro e continua com o próximo

                    # Criação do aluno
                    Aluno.objects.create(
                        nome=nome,
                        id_carteirinha=id_carteirinha,
                        id_curso=curso
                    )
                except IndexError:
                    print("Erro: O arquivo CSV está com formato incorreto.")
                    return redirect("criar_aluno")

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


@login_required
def relatorio(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH frequencias_calculadas AS (
                SELECT 
                    f.id_aluno_id,
                    f.data,
                    f.hora,
                    LEAD(f.hora) OVER (PARTITION BY f.id_aluno_id, f.data ORDER BY f.hora) AS proxima_hora,
                    CAST(f.identificador AS INTEGER) AS identificador,
                    CASE 
                        WHEN CAST(f.identificador AS INTEGER) = 2 
                        AND NOT EXISTS (
                            SELECT 1
                            FROM web_frequencia f2 
                            WHERE f2.id_aluno_id = f.id_aluno_id 
                            AND f2.data = f.data 
                            AND CAST(f2.identificador AS INTEGER) = 1
                        ) THEN true
                        ELSE false
                    END as apenas_saida
                FROM 
                    web_frequencia AS f
            ),
            atrasos_aluno AS (
                SELECT 
                    aluno.id_carteirinha,
                    aluno.nome,
                    c.turma,
                    COUNT(DISTINCT CASE WHEN f.hora > c.horario_entrada + INTERVAL '10 minutes' AND CAST(COALESCE(f.identificador, 0) AS INTEGER) = 1 THEN f.data END) AS total_atrasos,
                    COUNT(DISTINCT f.data) AS dias_presenca,
                    c.dias_letivos
                FROM 
                    web_aluno AS aluno
                JOIN 
                    web_curso AS c ON aluno.id_curso_id = c.turma
                LEFT JOIN 
                    frequencias_calculadas AS f ON aluno.id_carteirinha = f.id_aluno_id
                    AND f.data BETWEEN c.data_inicio AND c.data_fim
                GROUP BY 
                    aluno.id_carteirinha, aluno.nome, c.turma, c.dias_letivos
            ),
            frequencia_aluno AS (
                SELECT
                    nome,
                    turma,
                    total_atrasos,
                    dias_presenca,
                    dias_letivos,
                    ROUND((dias_presenca::decimal / dias_letivos) * 100, 2) AS frequencia_porcentagem
                FROM 
                    atrasos_aluno
            ),
            top_atrasos AS (
                SELECT nome, turma, total_atrasos, frequencia_porcentagem
                FROM frequencia_aluno
                ORDER BY total_atrasos DESC
                LIMIT 5
            ),
            baixa_frequencia AS (
                SELECT nome, turma, total_atrasos, frequencia_porcentagem
                FROM frequencia_aluno
                ORDER BY frequencia_porcentagem ASC
                LIMIT 5
            )
            
            SELECT 
                'Top Atrasos' AS categoria, 
                nome, turma, total_atrasos, frequencia_porcentagem
            FROM 
                top_atrasos
            UNION ALL
            SELECT 
                'Baixa Frequência' AS categoria, 
                nome, turma, total_atrasos, frequencia_porcentagem
            FROM 
                baixa_frequencia
            ORDER BY 
                categoria, total_atrasos DESC, frequencia_porcentagem ASC;
        """)

        alunos_detalhes = cursor.fetchall()

    relatorio = []
    for aluno in alunos_detalhes:
        relatorio.append({
            'categoria': aluno[0],
            'nome': aluno[1],
            'turma': aluno[2],
            'total_atrasos': aluno[3],
            'frequencia_porcentagem': aluno[4],
        })

    buffer = BytesIO()
    
    objeto_pdf = canvas.Canvas(buffer)
    objeto_pdf.setTitle("Relatório")
    subTitle = "Subtítulo do Relatório"

    objeto_pdf.setFont("Times-Roman", 36)
    objeto_pdf.drawCentredString(300, 770, "Relatório geral")
    objeto_pdf.setFont("Times-Roman", 24)
    objeto_pdf.drawCentredString(290, 720, subTitle)

    dados_tabela = [['Categoria', 'Nome', 'Turma', 'Atrasos', 'Frequência (%)']]
    for aluno in relatorio:
        dados_tabela.append([
            aluno['categoria'],
            aluno['nome'],
            aluno['turma'],
            str(aluno['total_atrasos']),
            f"{aluno['frequencia_porcentagem']}%"
        ])

    tabela = Table(dados_tabela)

    tabela.wrapOn(objeto_pdf, 400, 600)
    tabela.drawOn(objeto_pdf, 100, 600)
    
    objeto_pdf.showPage()
    objeto_pdf.save()
    buffer.seek(0)

    context = {
        'relatorio': relatorio,
    }

    if request.GET.get('format') == 'pdf':
        return FileResponse(buffer, filename="relatorio.pdf")
    
    return render(request, 'relatorio.html', context)