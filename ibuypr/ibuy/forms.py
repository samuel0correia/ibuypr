from django import forms
from .models import Categoria, Produto, Comentario


#class CategoriaForm(forms.ModelForm):
 #   class Meta:
  #      model = Categoria
   #     fields = ['tipo']


class ProdutoForm(forms.ModelForm):
    img_produto = forms.ImageField(label='Imagem do Produto')
    class Meta:
        model = Produto
        fields = ['nome', 'quantidade', 'preco', 'descricao', 'condicao', 'categoria', 'img_produto']


class ComprarProdutoForm(forms.Form):
    quantidade = forms.IntegerField()


class ContaForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    apelido = forms.CharField(label='Apelido', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    cpassword = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput())
    img_user = forms.ImageField(label='Imagem de Utilizador')


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {
            'texto': "Insira comentario"
        }

