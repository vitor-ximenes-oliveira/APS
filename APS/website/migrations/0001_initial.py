# Generated by Django 3.2.13 on 2022-11-12 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=40)),
                ('dt_nascimento', models.DateField()),
                ('cargo', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('filial', models.CharField(max_length=20)),
                ('senha', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Funcionario',
            },
        ),
        migrations.CreateModel(
            name='Estacao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dia', models.IntegerField()),
                ('hora', models.TimeField()),
                ('estacao', models.CharField(max_length=20)),
                ('codigo', models.CharField(max_length=4)),
                ('poluente', models.CharField(max_length=2)),
                ('valor', models.FloatField()),
                ('unidade', models.CharField(max_length=2)),
                ('tipo', models.CharField(max_length=10)),
                ('idFuncionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.funcionario')),
            ],
            options={
                'db_table': 'Estacao',
            },
        ),
    ]
