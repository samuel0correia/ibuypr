from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime


class Utilizador(models.Model):
    # id ?
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=100, default='')
    # user_fk = models.ForeignKey() como se faz esta


class Produto(models.Model):
    # como crio um id para o produto?
    utilizador_fk = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    produto_name = models.CharField(max_length=100)
    categoria_fk = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    quantity = models.IntegerFields(default=0)  # ou 1?
    description = models.TextField()  # mudar
    image_name = models.CharField(max_length=100, default='')
    #condition_state = models.BooleanFied(default=True)  # true->novo false->usado || secalhar a outro Field melhor
    NOVO = 'novo'
    USADO = 'usado'
    CONDITION_CHOICES = (
        (NOVO, _('Novo')),
        (USADO, _('Usado')),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, default=NOVO)

class Categoria(models.Model):
    # id?
    ROUPA = 'roupa'
    LIVROS = 'livros' # nao sei se posso escrver mais
    SEBENTAS = 'sebentas'
    CASA = 'casa'
    CATEGORIA_CHOICES = (
        (ROUPA, _('Roupa')),
        (LIVROS, _('Livros e Cadernos')),
        (SEBENTAS, _('Apontamentos e Sebentas')),
        (CASA, _('Casa')),
    )
    categoria_name = models.CharField(choices=CATEGORIA_CHOICES)  # definir o default

class Rating(models.Model):
    None
    # https://django-star-ratings.readthedocs.io/en/latest/
    # Checkem isto e digam se gostam ou nao

class Comentario(models.Model):
    # nao sei como fzr both ids
    comentario_text = models.TextField()