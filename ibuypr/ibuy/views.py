from django.shortcuts import render


def index(request):
    return render(request, 'ibuy/index.html')

def minhaconta(request):
    return render(request, 'ibuy/minhaconta.html')

def perfil(request):
    return render(request, 'ibuy/perfil.html')

def produto(request):
    return render(request, 'ibuy/produto.html')

def carrinho(request):
    return render(request, 'ibuy/carrinho.html')

def meusprodutos(request):
    return render(request, 'ibuy/meusprodutos.html')

def criarproduto(request):
    return render(request, 'ibuy/criarproduto.html')

# Create your views here.
