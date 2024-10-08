# Generated by Django 5.1.1 on 2024-10-08 16:34

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='dias_funcionamento',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('SEG', 'Segunda-feira'), ('TER', 'Terça-feira'), ('QUA', 'Quarta-feira'), ('QUI', 'Quinta-feira'), ('SEX', 'Sexta-feira')], max_length=3), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cargo',
            field=models.CharField(choices=[('COORDENACAO', 'Coordenacao'), ('ADMINISTRAÇÃO', 'Administração')], max_length=15),
        ),
    ]
