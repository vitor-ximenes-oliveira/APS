import os
import stat
import subprocess as sp
from stat import S_IREAD

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import NoReverseMatch, reverse
from django.utils.datastructures import MultiValueDictKeyError

from SAE import settings
from SAE.settings import BASE_DIR, MEDIA_ROOT
from website.models import Estacao, Funcionario


def cadastroFuncionario(request):
    if request.method == 'POST':
        try:
                email = request.POST.get("email")
                checar_email = Funcionario.objects.get(email = email)
                if checar_email:
                    messages.error(request, "Já existe um funcionário cadastrado com esse e-mail")          
        except (Funcionario.DoesNotExist):
                    email = request.POST.get("email")
                    dt_nascimento = request.POST.get("dt_nascimento") 
                    nome = request.POST.get("nome")
                    cargo = request.POST.get("cargo")
                    filial = request.POST.get("filial")
                    senha = request.POST.get("senha")            
                    confir_senha = request.POST.get("confir_senha")
                    try:
                        if senha != confir_senha:
                            messages.error(request,"As senhas inseridas são diferentes")
                            return redirect("/Teladecadastroaluno")
                        else:
                            al_senha = make_password(senha)
                            autenticar_usuario = User(username=nome, password=senha)                          
                            autenticar_usuario.save()       
                            user = Funcionario.objects.create(nome=nome, email=email,dt_nascimento=dt_nascimento,cargo=cargo,filial=filial, al_senha=al_senha)
                            messages.success(request,"Funcionário cadastrado com sucesso")                      
                            return redirect('login')
                    except (ValueError,ValidationError):
                        messages.error(request, "Data de nascimento inválida")  
                    except AttributeError:
                        messages.error(request,"Preencha os campos com dados válidos")
                    except (Funcionario.MultipleObjectsReturned):  
                        messages.error(request,"Preencha todos os campos") 
                    except (IntegrityError):
                        messages.error(request,"Já existe um funcionário cadastrado com esse nome")
    return render(request,'cadastroFuncionario.html')

def loginFuncionario(request):      
            if 'login' in request.POST:        
                    nome = request.POST.get("nome")
                    senha = request.POST.get("senha")

                    if not nome or not senha:
                        messages.error(request, "Preencha todos os campos")
                        return redirect('login')     
                    try:    
                            nome = request.POST.get("nome")
                            senha = request.POST.get("senha")    
                            funcionario = Funcionario.objects.get(nome=nome)            
                            usuario = User.objects.get(username=nome)
                            
                            if funcionario:
                                checar_senha=check_password(senha, usuario.password)
                                if checar_senha:
                                    autenticar_usuario = authenticate(username=nome, password=senha, backend= 'django.contrib.auth.backends.AllowAllUsersModelBackend')                    
                                    login(request, autenticar_usuario)
                                    return redirect('telaAluno/'+str(funcionario.id)) 

                    except(Funcionario.DoesNotExist,User.DoesNotExist):
                        messages.error(request,"Não existe um funcionário com esses nome e/ou senha")
                        

            elif 'cadastro' in request.POST:
                return redirect('/Teladecadastroaluno')
            return render(request,"Login.html")

def Dados(request, id):
    try:
        dados = Estacao.objects.filter(idFuncionario=id)
        if "adicionar" in request.POST:
            dia = request.POST.get("dia")
            hora = request.POST.get("hora")
            estacao = request.POST.get("estacao")
            codigo = request.POST.get("codigo")
            poluente = request.POST.get("poluente")
            valor = request.POST.get("valor")
            unidade = request.POST.get("unidade")
            tipo = request.POST.get("tipo")
            func = Funcionario()
            func.id = id
            chaveFuncionario = Funcionario.objects.get(id=id)
            inserir_dados = Estacao.objects.create(dia=dia,hora=hora,estacao=estacao,codigo=codigo,poluente=poluente,valor=valor,unidade=unidade,tipo=tipo,idFuncionario=chaveFuncionario)
            messages.success(request,"Dado adicionado com sucesso")
            return redirect('../Dados/'+str(id))
        elif "editar" in request.POST:
            dia = request.POST.get("dia")
            hora = request.POST.get("hora")
            estacao = request.POST.get("estacao")
            codigo = request.POST.get("codigo")
            poluente = request.POST.get("poluente")
            valor = request.POST.get("valor")
            unidade = request.POST.get("unidade")
            tipo = request.POST.get("tipo")
            editar_dados = Estacao.objects.filter(id=id).update(dia=dia,hora=hora,estacao=estacao,codigo=codigo,poluente=poluente,
            valor=valor,unidade=unidade,tipo=tipo)
            messages.success(request,"Dado editado com sucesso")
            return redirect('../Dados/'+str(id)) 
        elif "excluir" in request.POST:
            apagarDado = Estacao.objects.filter(id=id).delete()
            messages.success(request,"Dado excluído com sucesso")
            return redirect('../Dados/'+str(id)) 
    except ValueError:
        messages.error(request,"Preencha todos os campos")
    except ValidationError:
        messages.error(request,"Insira um horário")
    return render(request,'Dados.html',{'dados':dados,'id':id})


def visualizar_arquivo(request,arquivo):
    try:
        extensoes = [".pdf", ".txt", ".png", ".jpg", ".gif", ".bmp",".mp3",".mp4",'.JPG']
        if arquivo.endswith(tuple(extensoes)):
            diretorio_arquivo = os.path.join(settings.MEDIA_ROOT, arquivo)
            arquivo = open(diretorio_arquivo, 'rb') 
            abrir_Arquivo = FileResponse(arquivo)
            return abrir_Arquivo
        elif arquivo.endswith('.docx'): 
            diretorio_arquivo = os.path.join(settings.MEDIA_ROOT, arquivo)        
            sp.Popen(["C:\Program Files\Windows NT\Accessories\WordPad.exe", diretorio_arquivo])
            os.chmod(diretorio_arquivo,stat.S_IWUSR and stat.S_IRUSR and stat.S_IRUSR)  
            fk_aluno = request.GET.get("alu",'')      
            return redirect('../atividades/'+str(fk_aluno))
        else:
            diretorio_arquivo = os.path.join(settings.MEDIA_ROOT, arquivo)
            os.system(diretorio_arquivo)    
            os.chmod(diretorio_arquivo,S_IREAD)  
            fk_aluno = request.GET.get("alu",'')      
            return redirect('../atividades/'+str(fk_aluno))
    except(FileNotFoundError,ValueError):
            messages.error(request,"Arquivo não encontrado")
            fk_aluno = request.GET.get("alu",'')      
            return redirect('../atividades/'+str(fk_aluno))

def baixar_arquivo(request, arquivo):
    try:
        if arquivo != '':
            diretorio_arquivo = (os.path.join(settings.MEDIA_ROOT, arquivo))
            diretorio = open(diretorio_arquivo,'rb')
            download_arquivo = HttpResponse(diretorio ,content_type="aplicacao/arquivo")
            download_arquivo ['Content-Disposition'] = "attachment; nome_arquivo=" + arquivo
            return download_arquivo
        else:
            messages.error(request,"Arquivo não encontrado")
            return redirect('../atividades/'+str(fk_aluno))
    except(FileNotFoundError,ValueError):
            messages.error(request,"Arquivo não encontrado")
            fk_aluno = request.GET.get("alu",'')      
            return redirect('../atividades/'+str(fk_aluno))
    
#@login_required(login_url='/login')

def sair(request):
        logout(request)
        messages.success(request,"Você saiu do seu perfil")
        return HttpResponseRedirect("/")







