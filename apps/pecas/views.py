from django.shortcuts import render, redirect, get_object_or_404
from pecas.models import Peca, ProdutoPeca
from sku.models import Sku, Sufixo
from django.contrib import messages
from django.contrib.messages import constants
from django.http import JsonResponse, HttpResponse
from produto.models import Produto
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
@login_required(login_url='logar')
def verificar_sku(request):
    if request.method == 'POST':
        sku_digitado = request.POST.get('sku')

        # Verificar se o SKU existe
        if sku_digitado is not None:
            try:
                sku_instance = Sku.objects.get(sku=sku_digitado)
                return redirect('cadastrar_peca', sku=sku_instance.sku)
            except Sku.DoesNotExist:
                messages.error(request, "SKU não encontrado.")
                return redirect('verificar_sku')

    return render(request, 'verificar_sku.html')

# Página 2: Formulário para Cadastrar a Peça
@login_required(login_url='logar')
def cadastrar_pecas(request, sku):
    try:
        sku_instance = Sku.objects.get(sku=sku)
    except Sku.DoesNotExist:
        return HttpResponse("SKU não encontrado", status=404)

    if request.method == 'POST':
        sufixo = request.POST.get('sufixo')
        part_number = request.POST.get('part_number').upper()
        
        descricao = request.POST.get('descricao').upper()
        observacao = request.POST.get('observacao')
        posicao = request.POST.get('posicao')
        defeito_pecas = request.POST.get('defeito_pecas')
        # Verifica se o sufixo pertence ao SKU
        try:
            sufixo_instance = Sufixo.objects.get(sufixo=sufixo, sku=sku_instance)
        except Sufixo.DoesNotExist:
            messages.error(request, 'Sufixo não encontrado para o SKU.')
            return redirect('cadastrar_pecas', sku=sku_instance.sku)
        
        

        if Peca.objects.filter(part_number=part_number).exists():
            messages.add_message(request, constants.ERROR, 'Já existe uma peça com esse part number')  
        else:             
            peca = Peca(
                sku=sku_instance,
                sufixo=sufixo_instance,
                part_number=part_number,
                descricao=descricao,
                posicao=posicao,
                observacao=observacao,
                defeito_pecas=defeito_pecas
            )
            peca.save() 

        messages.success(request, 'Peça cadastrada com sucesso.')
          # Ou redirecionar para outra página

    # Buscar os sufixos relacionados ao SKU
    sufixos = Sufixo.objects.filter(sku=sku_instance)

    return render(request, 'cadastrar_pecas.html', {
        'sku': sku_instance.sku,
        'sufixos': sufixos,
    })

@login_required(login_url='logar')
def buscar_produto(request):
    if request.method == "GET":
        return render(request, "buscar_produto.html")

    elif request.method == "POST":
        procura = request.POST.get("procura", "").strip()
        if procura:
            produto = Produto.objects.filter(ptn__icontains=procura).first()
            if produto:
                pecas = Peca.objects.filter(sufixo=produto.sufixo)  # Filtra peças compatíveis pelo sufixo
                return render(request, "buscar_produto.html", {"produto": produto, "pecas": pecas})

        return render(request, "buscar_produto.html", {"erro": "Produto não encontrado!"})

@login_required(login_url='logar')
def adicionar_pecas(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        with transaction.atomic():  
            
            produto.status = "VERIFICAR DISPONIBILIDADE"
            produto.save()

            
            pecas_selecionadas = request.POST.getlist("pecas")

            ProdutoPeca.objects.filter(produto=produto).exclude(peca_id__in=pecas_selecionadas).delete()
            
            pecas = {p.id: p for p in Peca.objects.filter(id__in=pecas_selecionadas)}
            
            for peca_id in pecas_selecionadas:
                peca = pecas.get(int(peca_id))

                if peca:
                    tipo = request.POST.get(f"tipo_peca_{peca.id}", "")
                    defeito = request.POST.get(f"defeito_pecas_{peca.id}", "")

                    ProdutoPeca.objects.update_or_create(
                        produto=produto,
                        peca=peca,
                        defaults={"tipo_peca": tipo, "defeito_pecas": defeito}
                    )

            
            if not ProdutoPeca.objects.filter(produto=produto).exists():
                produto.status = "LIBERADO PARA CONSERTO"
                produto.save()

        return redirect("buscar_produto") 
    
    return redirect("buscar_produto")


   )