from django.shortcuts import render, redirect
from .models import Funcionario
from django.contrib import messages
from django.contrib.messages import constants


# Create your views here.

def cad_funcionario(request):
      
    if request.method == "GET":
            
        return render(request, 'cad_funcionario.html')

    elif request.method == "POST": 
       
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')
        cod = request.POST.get('cod')

        try:
            funcionario = Funcionario.objects.create(nome=nome, cargo=cargo, cod=cod)
            messages.add_message(request, constants.SUCCESS, 'Funcionario Cadastrado')
            return redirect('cad_funcionario')
        except:
            messages.add_message(request, constants.SUCCESS, 'Funcionario já Existe')
            return redirect('cad_funcionario') 
