from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'ibuy/index.html')


def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not (username and password):
            # request.session['varerro'] = 'Não preencheu todos os campos'
            return HttpResponseRedirect(reverse('ibuy:index'))
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #request.session['varerro'] = None
            return HttpResponseRedirect(reverse('ibuy:index'))
        else:
            #request.session['varerro'] = 'Username ou password errada'
            return HttpResponseRedirect(reverse('ibuy:loginuser'))
    return render(request, 'ibuy/loginuser.html')


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def minhaconta(request):
    return render(request, 'ibuy/minhaconta.html')


def perfil(request):
    return render(request, 'ibuy/perfil.html')


def produto(request):
    return render(request, 'ibuy/produto.html')


def carrinho(request):
    return render(request, 'ibuy/carrinho.html')


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def meusprodutos(request):
    return render(request, 'ibuy/meusprodutos.html')


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def criarproduto(request):
    return render(request, 'ibuy/criarproduto.html')

# Create your views here.
