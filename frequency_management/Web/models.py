from django.db import models

TIPO_USUARIOS = (
    ("COORDENACAO", "Coordenacao"),
    ("ADMINISTRAÇÃO", "Administração")
)

class Senai(models.Model):
    nome_instituicao = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="")
    endereco = models.CharField(max_length=150)
    telefone = models.IntegerField()

    def __str__(self):
        return self.nome_instituicao

class Curso(models.Model):
    id = models.AutoField(primary_key=True) 
    nome_curso = models.CharField(max_length=20)
    horario_entrada = models.TimeField()
    horario_saida = models.CharField(max_length=20)
    responsavel = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_curso

class Aluno(models.Model):
    nome = models.CharField(max_length=50)
    id_carteirinha = models.IntegerField(primary_key=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE) 

    def __str__(self):
        return self.nome

class Frequencia(models.Model):
    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    horario_entrada = models.TimeField()
    horario_saida = models.TimeField()
    data = models.DateField()

    def __str__(self):
        return f"Frequência de {self.id_aluno} em {self.data}"

class Usuario(models.Model):
    nome = models.CharField(max_length=60)
    sobrenome = models.CharField(max_length=60)
    username = models.CharField(max_length=20, primary_key=True)
    senha = models.CharField(max_length=20)
    cargo = models.CharField(max_length=15, choices=TIPO_USUARIOS)

    def __str__(self):
        return self.username
