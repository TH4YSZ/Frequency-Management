# Generated by Django 5.1.1 on 2024-10-17 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_aluno_id_carteirinha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='id_carteirinha',
            field=models.CharField(primary_key=True, serialize=False),
        ),
    ]
