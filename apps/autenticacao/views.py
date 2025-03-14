from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password

# Create your views here.
def logar(request):
    if request.method =="GET":
        logout(request)
        return render(request, 'login_cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('nome')
        password = request.POST.get('senha')

        usuario = authenticate(username=username, password=password)
        print (usuario)
        if usuario:
            login(request, usuario)
            return redirect('home')  # Substitua 'home' pela URL nomeada desejada

        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
        return render(request, 'login_cadastro.html')
    
    return render(request, 'login_cadastro.html')


def cadastro(request):
    if request.method =="GET":
        return render(request, 'login_cadastro.html')
    elif request.method =="POST":
        
       nome = request.POST.get('nome')
       senha = request.POST.get('senha')
       confirmar_senha = request.POST.get('confirmar_senha')

    if Usuario.objects.filter(username=nome).exists():
        messages.add_message(request, constants.ERROR, 'Usuário já existe')
        return render(request, 'login_cadastro.html')
    elif senha != confirmar_senha:
        messages.add_message(request, constants.ERROR, 'As senhas não são iguais')
        return render(request, 'login_cadastro.html')

    usuario = Usuario(username=nome)
    usuario.set_password(senha)
    usuario.save()
    messages.add_message(request, constants.SUCCESS, 'Usuário Cadastrado')
    return render(request, 'login_cadastro.html')
    
def sair(request):
    
    logout(request)
    return render(request, 'login_cadastro.html')




