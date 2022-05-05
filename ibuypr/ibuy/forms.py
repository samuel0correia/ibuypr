from django import forms
from .models import Categoria, Produto


#class CategoriaForm(forms.ModelForm):
 #   class Meta:
  #      model = Categoria
   #     fields = ['tipo']


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'quantidade', 'preco', 'descricao', 'condicao', 'categoria', 'nome_imagem']
