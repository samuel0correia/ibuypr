from django import forms
from django.contrib.auth.models import User

from .models import Categoria, Produto, Comentario, Utilizador


#class CategoriaForm(forms.ModelForm):
 #   class Meta:
  #      model = Categoria
   #     fields = ['tipo']


class ProdutoForm(forms.ModelForm):
    img_produto = forms.ImageField(label='Imagem do Produto', required=False)
    class Meta:
        model = Produto
        widgets = {
            'quantidade':forms.NumberInput(attrs={'min':0}),
            'preco':forms.NumberInput(attrs={'min':0.00 , 'max':9999.99} )
        }
        fields = ['nome', 'quantidade', 'preco', 'descricao', 'condicao', 'categoria', 'video_embed', 'img_produto']


class ContaForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    apelido = forms.CharField(label='Apelido', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    cpassword = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput())
    img_user = forms.ImageField(label='Imagem de Utilizador')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = ['username', 'first_name', 'last_name', 'email']


class UtilizadorForm(forms.ModelForm):
    img_utilizador = forms.ImageField(label='Imagem do Utilizador', required=False)
    class Meta:
        model = Utilizador
        fields = ['img_utilizador']


class PasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    cpassword = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput())


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {
            'texto': "Insira comentario"
        }

