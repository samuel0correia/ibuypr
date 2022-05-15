from django import forms
from django.contrib.auth.models import User

from .models import Categoria, Produto, Comentario, Utilizador


#class CategoriaForm(forms.ModelForm):
 #   class Meta:
  #      model = Categoria
   #     fields = ['tipo']


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'quantidade', 'preco', 'descricao', 'condicao', 'categoria', 'video_embed', 'imagem']
        labels = {
            'nome': 'Nome',
            'quantidade': 'Quantidade',
            'preco': 'Preço',
            'descricao': 'Descrição',
            'condicao': 'Condição',
            'categoria': 'Categoria',
            'video_embed': 'Código embed do vídeo',
            'imagem': 'Imagem',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-field'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-field', 'min':0}),
            'preco': forms.NumberInput(attrs={'class': 'form-field', 'min':0.00 , 'max':9999.99}),
            'descricao': forms.TextInput(attrs={'class': 'form-field form-bigger-field'}),
            'condicao': forms.Select(attrs={'class': 'form-field form-select-field'}),
            'categoria': forms.Select(attrs={'class': 'form-field form-select-field'}),
            'video_embed': forms.TextInput(attrs={'class': 'form-field'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'input-file'}),
        }

class ComprarProdutoForm(forms.Form):
    quantidade = forms.IntegerField()


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
            'email': forms.EmailInput(attrs={'class': 'form-field'}),
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
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'form-field', 'placeholder': 'Adicione um comentário...', 'width': '100%'}),
        }

