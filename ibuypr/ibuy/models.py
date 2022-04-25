from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_imagem = models.CharField(max_length=100, default='user.png')
    # user_fk = models.ForeignKey() como se faz esta


class Produto(models.Model):
    utilizador_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    categoria_fk = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    quantidade = models.IntegerFields(default=0)  # ou 1?
    descricao = models.TextField()  # mudar
    nome_imagem = models.CharField(max_length=100, default='') #possivelmente vamos querer permitir mais que 1 imagem
    #condition_state = models.BooleanFied(default=True)  # true->novo false->usado || secalhar a outro Field melhor
    NOVO = 'novo'
    USADO = 'usado'
    OPCOES_CONDICAO = (
        (NOVO, _('Novo')),
        (USADO, _('Usado')),
    )
    condicao = models.CharField(choices=OPCOES_CONDICAO, default=NOVO)

class Categoria(models.Model):
    ROUPA = 'roupa'
    ESCRITA = 'escrita' # nao sei se posso escrver mais
    CANETAS = 'canetas'
    SEBENTAS = 'sebentas'
    CASA = 'casa'
    OUTROS = 'outros'
    OPCOES_CATEGORIA = (
        (ROUPA, _('Roupa')),
        (LIVROS, _('Livros e Cadernos')),
        (ESCRITA, _('Material de Escrita')),
        (SEBENTAS, _('Apontamentos e Sebentas')),
        (CASA, _('Casa')),
        (OUTROS, _('Outros')),
    )
    nome = models.CharField(choices=OPCOES_CATEGORIA, default=OUTROS)  # definir o default

class Rating(models.Model):
    None
    # https://django-star-ratings.readthedocs.io/en/latest/
    # Checkem isto e digam se gostam ou nao
    # ter uma coisa logo completa seria muito bom, só não percebi muito bem como funciona.

class Comentario(models.Model):
    utilizador_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    produto_fk = models.ForeignKey(Produto, on_delete=models.CASCADE)
    #os comentarios são para os produtos, right?
    texto = models.TextField()
    #data?