from django.db import models

TIPO_USUARIOS = (
    ("COORDENADOR", "Coordenador"),
    ("PROFESSOR", "Professor")
)

class Senai(models.Model):
    nome_instituicao = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="")
    endereco = models.CharField(max_length=150)
    telefone = models.IntegerField()

    def __str__(self):
        return self.nome_instituicao

class Aluno(models.Model):
    nome = models.CharField(max_length=50)
    id_carteirinha = models.IntegerField()
    id_curso = models.IntegerField()
    nome_curso = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Frequencia(models.Model):
    id_aluno = models.IntegerField()
    horario_entrada = models.TimeField()
    horario_saida = models.TimeField()
    data = models.DateField()

    def __str__(self):
        return f"Frequência de {self.id_aluno} em {self.data}"

class Curso(models.Model):
    id_curso = models.IntegerField()
    nome_curso = models.CharField(max_length=20)
    horario_entrada = models.TimeField()
    horario_saida = models.CharField(max_length=20)
    responsavel = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_curso

class Usuario(models.Model):
    nome = models.CharField(max_length=60)
    sobrenome = models.CharField(max_length=20)
    nome_usuario = models.CharField(max_length=20)
    senha = models.CharField(max_length=20)
    cargo = models.CharField(max_length=15)

    def __str__(self):
        return self.nome_usuario
