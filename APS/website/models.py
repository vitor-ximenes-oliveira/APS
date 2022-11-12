
import os
from datetime import *

from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Funcionario(models.Model):
    id = models.AutoField(primary_key = True)
    nome = models.CharField(max_length=40)
    dt_nascimento = models.DateField()
    cargo = models.CharField(max_length=15)
    email = models.EmailField()
    filial = models.CharField(max_length=20)
    senha = models.CharField
    class Meta:
        db_table = "Funcionario"

class Estacao(models.Model):
    id = models.AutoField(primary_key=True)
    dia = models.DateField()
    hora = models.TimeField()
    estacao = models.CharField(max_length=20,blank = False)
    codigo = models.CharField(max_length=4,blank = False)
    poluente = models.CharField(max_length=2,blank = False)
    valor = models.FloatField()
    unidade = models.CharField(max_length=2,blank = False)
    tipo = models.CharField(max_length=10,blank = False)
    idFuncionario = models.ForeignKey(Funcionario,blank= False,on_delete = models.CASCADE)
    class Meta:
        db_table = 'Estacao'

User._meta.get_field('username').validators=[validators.RegexValidator(r'^[\w.@+ ]+$', _('Digite um nome válido.'), 'Inválido')]
