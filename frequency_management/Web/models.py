from django.db import models
from django.contrib.postgres.fields import ArrayField


TIPO_USUARIOS = (
    ("COORDENACAO", "Coordenacao"),
    ("ADMINISTRAÇÃO", "Administração")
)

DIAS_DA_SEMANA = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira')
    ]

class Senai(models.Model):
    nome_instituicao = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="")
    endereco = models.CharField(max_length=150)
    telefone = models.IntegerField()

    def __str__(self):
        return self.nome_instituicao

class Curso(models.Model):
    turma = models.CharField(max_length=100, primary_key=True)
    nome_curso = models.CharField(max_length=100)
    horario_entrada = models.TimeField()
    horario_saida = models.TimeField()
    carga_horaria = models.IntegerField(default=1200)
    responsavel = models.CharField(max_length=100)
    dias_funcionamento = ArrayField(
        models.CharField(max_length=3, choices=DIAS_DA_SEMANA),
        blank=True,
        default=list
    )
    data_inicio = models.DateField(default='2024-01-26')
    data_fim = models.DateField(default='2024-12-17')
    carga_horaria_intervalo = models.TimeField(default='02:00:00')
    dias_letivos = models.IntegerField(default='80')


    def __str__(self):
        return self.nome_curso


class Aluno(models.Model):
    nome = models.CharField(max_length=150)
    id_carteirinha = models.CharField(primary_key=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Frequencia(models.Model):
    id = models.AutoField(primary_key=True)
    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    identificador = models.IntegerField()

    def __str__(self):
        return f"Frequência de {self.id_aluno} em {self.data}"

class Usuario(models.Model):
    nome = models.CharField(max_length=60)
    sobrenome = models.CharField(max_length=60)
    username = models.CharField(max_length=20, primary_key=True)
    cargo = models.CharField(max_length=15, choices=TIPO_USUARIOS)

    def __str__(self):
        return self.username