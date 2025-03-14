from django.db import models
from funcionario.models import Funcionario
from sku.models import Sku, Sufixo
from pecas.models import Peca  # Aqui mantemos apenas Peca, sem ProdutoPeca ainda

class Produto(models.Model):
    STATUS_CHOICES = [
        ('ENTRADA', 'ENTRADA'),
        ('TRIAGEM', 'TRIAGEM'),
        ('CONSERTO', 'CONSERTO'),
        ('VERIFICAR DISPONIBILIDADE', 'VERIFICAR DISPONIBILIDADE'),
        ('AGUARDANDO PEÇA', 'AGUARDANDO PEÇA'),
        ('LIBERADO PARA CONSERTO', 'LIBERADO PARA CONSERTO'),
        ('EMBALAGEM', 'EMBALAGEM'),
        ('ENCERRADO', 'ENCERRADO'),
    ]
    DEFEITO_CHOICES = [
        ('Estético', 'Estético'),
        ('Funcional', 'Funcional'),
        ('Estético-Funcional', 'Estético-Funcional'),
        ('Sem Defeito', 'Sem Defeito'),
        ('Venda Direta', 'Venda Direta'),
    ]

    DEFEITO_ESPECIFICO = [
        ('Tela Quebrada', 'Tela Quebrada'),
        ('Não liga', 'Não liga'),
        ('Sem Defeito', 'Sem Defeito'),
    ]

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='ENTRADA')
    data_entrada = models.DateTimeField(auto_now_add=True)
    observacao = models.CharField(max_length=100, blank=True)
    ptn = models.CharField(max_length=15)
    serie = models.CharField(max_length=30)
    sku = models.ForeignKey(Sku, on_delete=models.DO_NOTHING, related_name="produto_sku")
    sufixo = models.ForeignKey(Sufixo, on_delete=models.DO_NOTHING, related_name="produto_sufixo")
    modelo = models.ForeignKey(Sku, on_delete=models.DO_NOTHING, related_name="produto_modelo_sku")
    peca = models.ManyToManyField('pecas.Peca', through="pecas.ProdutoPeca", related_name="produtos")
    defeito = models.CharField(max_length=30, choices=DEFEITO_CHOICES, null=False, blank=False)
    defeito_especifico = models.CharField(max_length=30, choices=DEFEITO_ESPECIFICO, default="Sem Defeito")
    responsavel_conserto = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, related_name="responsavel_conserto"
    )
    responsavel_embalagem = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, related_name="responsavel_embalagem"
    )
    responsavel_entrada = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, related_name="responsavel_entrada"
    )
    responsavel_saida = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, related_name="responsavel_saida"
    )
    responsavel_triagem = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, related_name="responsavel_triagem"
    )

    @property
    def tipo_defeito(self):
        for chave, valor in self.DEFEITO_CHOICES:
            if chave == self.defeito:
                return valor
        return 'Desconhecido'

    def __str__(self):
        return f"{self.status} | {self.data_entrada} | {self.ptn} | {self.serie} | {self.sku} | {self.sufixo} | {self.modelo} | {self.responsavel_conserto} | {self.responsavel_embalagem} | {self.responsavel_entrada} | {self.responsavel_triagem} | {self.responsavel_saida} | {self.defeito}"
