# Generated by Django 5.1.1 on 2024-10-24 11:20

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('turma', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('nome_curso', models.CharField(max_length=100)),
                ('horario_entrada', models.TimeField()),
                ('horario_saida', models.CharField(max_length=20)),
                ('carga_horaria', models.IntegerField(default=1200)),
                ('responsavel', models.CharField(max_length=100)),
                ('dias_funcionamento', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('SEG', 'Segunda-feira'), ('TER', 'Terça-feira'), ('QUA', 'Quarta-feira'), ('QUI', 'Quinta-feira'), ('SEX', 'Sexta-feira')], max_length=3), blank=True, default=list, size=None)),
                ('data_inicio', models.DateField(default='2024-01-26')),
                ('data_fim', models.DateField(default='2024-12-17')),
            ],
        ),
        migrations.CreateModel(
            name='Senai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_instituicao', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='')),
                ('endereco', models.CharField(max_length=150)),
                ('telefone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('nome', models.CharField(max_length=60)),
                ('sobrenome', models.CharField(max_length=60)),
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('senha', models.CharField(max_length=20)),
                ('cargo', models.CharField(choices=[('COORDENACAO', 'Coordenacao'), ('ADMINISTRAÇÃO', 'Administração')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('nome', models.CharField(max_length=150)),
                ('id_carteirinha', models.CharField(primary_key=True, serialize=False)),
                ('id_curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('identificador', models.IntegerField()),
                ('id_aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.aluno')),
            ],
        ),
    ]
