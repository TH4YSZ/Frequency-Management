# Generated by Django 5.1.1 on 2024-09-19 13:47

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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome_curso', models.CharField(max_length=20)),
                ('horario_entrada', models.TimeField()),
                ('horario_saida', models.CharField(max_length=20)),
                ('responsavel', models.CharField(max_length=20)),
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
                ('cargo', models.CharField(choices=[('COORDENAÇÃO', 'Coordenação'), ('ADMINISTRAÇÃO', 'Administração')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('nome', models.CharField(max_length=50)),
                ('id_carteirinha', models.IntegerField(primary_key=True, serialize=False)),
                ('id_curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario_entrada', models.TimeField()),
                ('horario_saida', models.TimeField()),
                ('data', models.DateField()),
                ('id_aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.aluno')),
            ],
        ),
    ]
