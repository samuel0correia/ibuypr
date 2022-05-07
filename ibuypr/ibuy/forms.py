from django import forms
from .models import Categoria, Produto


#class CategoriaForm(forms.ModelForm):
 #   class Meta:
  #      model = Categoria
   #     fields = ['tipo']


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'quantidade', 'preco', 'descricao', 'condicao', 'categoria']


class ComprarProdutoForm(forms.Form):
    quantidade = forms.IntegerField()


class ContaForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    apelido = forms.CharField(label='Apelido', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    cpassword = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput())
    img_user = forms.FileField(label='Imagem de Utilizador',
                               widget=forms.FileInput(attrs={'accept': 'image/png, image/gif, image/jpeg'}))
