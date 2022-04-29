from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import Utilizador, Produto, Categoria
from .forms import ProdutoForm, CategoriaForm


def index(request):
    lista_produtos = Produto.objects.exclude(user_id=request.user.id)
    context = {'lista_produtos': lista_produtos}
    return render(request, 'ibuy/index.html', context)


def criarconta(request):
    if request.method == 'POST' and request.FILES['myfile']:
        nome = request.POST['nome']
        apelido = request.POST['apelido']
        email = nome + "@iscte.pt"
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES['myfile']
        if not (nome and apelido and username and password):
            return render(request, 'ibuy/criarconta.html', {'error_message': "Não completou todos os campos!"})
        if User.objects.filter(username=username).exists():
            return render(request, 'ibuy/criarconta.html',
                          {'error_message_2': "Já existe uma conta com esse username associado"})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = nome
            user.last_name = apelido
            user.save()
            FileSystemStorage().save(image.name, image)
            utilizador = Utilizador(user=user, nome_imagem=image.name)
            utilizador.save()
            return HttpResponseRedirect(reverse('ibuy:index'))
    else:
        return render(request, 'ibuy/criarconta.html')


def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not (username and password):
            return render(request, 'ibuy/loginuser.html', {'error_message': "Nao preencheu todos os campos!"})
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session.flush()
            login(request, user)
            return HttpResponseRedirect(reverse('ibuy:index'))
        else:
            request.session['invalid_user'] = 'Utilizador não existe, tente de novo com outro username/password'
            return HttpResponseRedirect(reverse('ibuy:loginuser'))
    else:
        return render(request, 'ibuy/loginuser.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('ibuy:index'))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def minhaconta(request):
    return render(request, 'ibuy/minhaconta.html')


def perfil(request):
    return render(request, 'ibuy/perfil.html')


def produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'ibuy/produto.html', {'produto':produto})


def carrinho(request):
    return render(request, 'ibuy/carrinho.html')


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def meusprodutos(request):
    lista_produtos = Produto.objects.filter(user_id=request.user.id)
    context = {'lista_produtos': lista_produtos}
    return render(request, 'ibuy/meusprodutos.html', context)


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def criarproduto(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        quantidade = request.POST['quantidade']
        preco = request.POST['preco']
        descricao = request.POST['descricao']
        condicao = request.POST['condicao']
        #imagem = request.FILES['myfile']
        #FileSystemStorage().save(imagem.name, imagem)
        tipo = request.POST['tipo']
        tipo_categoria = Categoria(tipo=tipo)
        tipo_categoria.save()
        produto = Produto(nome=nome, categoria=tipo_categoria, quantidade=quantidade, preco=preco, descricao=descricao, condicao=condicao, user=request.user)
        produto.save()
        print(produto.user)
        return HttpResponseRedirect(reverse('ibuy:meusprodutos'))
    else:
        context = {}
        context['form'] = ProdutoForm
        context['form2'] = CategoriaForm
        return render(request, 'ibuy/criarproduto.html', context)


def apagarproduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    produto.delete()
    #return HttpResponseRedirect(reverse('ibuy:index'))
    return HttpResponseRedirect(reverse('ibuy:meusprodutos'))

def adicionarproduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

# Create your views here.
