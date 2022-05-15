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
        fields = ['nome', 'quantidade', 'preco', 'descricao', 'condicao', 'categoria', 'video_embed', 'img_produto']


class ComprarProdutoForm(forms.Form):
    quantidade = forms.IntegerField()


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
        labels = {
            'username': 'Username',
            'first_name': 'Nome',
            'last_name': 'Apelido',
            'email': 'E-mail',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-field'}),
            'first_name': forms.TextInput(attrs={'class': 'form-field'}),
            'last_name': forms.TextInput(attrs={'class': 'form-field'}),
            'email': forms.TextInput(attrs={'class': 'form-field'}),
        }


class UtilizadorForm(forms.Form):
    img_utilizador = forms.ImageField(label='Imagem de Perfil', required=False, widget=forms.ClearableFileInput(attrs={'class': 'input-file'}))
    # widget=forms.ClearableFileInput(attrs={'class': 'form-btn'})


class PasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-field'}))
    cpassword = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput(attrs={'class': 'form-field'}))

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {
            'texto': "Insira comentario"
        }

