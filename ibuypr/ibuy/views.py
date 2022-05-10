from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import Utilizador, Produto, Categoria, Comentario
from .forms import ProdutoForm, ComprarProdutoForm, ContaForm, ComentarioForm


def index(request):
    lista_produtos = Produto.objects.exclude(user_id=request.user.id)
    context = {'lista_produtos': lista_produtos}
    return render(request, 'ibuy/index.html', context)


# mudar / melhorar
def criarconta(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        apelido = request.POST['apelido']
        email = nome + "@iscte.pt"  # é isto que queremos?
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password != cpassword:
            return render(request, 'ibuy/criarconta.html',
                          {'form': ContaForm, 'error_message': "As passwords inseridas não são iguais!"})
        image = request.FILES['img_user']
        if not (nome and apelido and username and password and image):
            return render(request, 'ibuy/criarconta.html',
                          {'form': ContaForm, 'error_message': "Não preencheu todos os campos!"})
        if User.objects.filter(username=username).exists():
            return render(request, 'ibuy/criarconta.html',
                          {'form': ContaForm, 'error_message': "Já existe uma conta com esse username associado"})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = nome
            user.last_name = apelido
            user.save()
            nome_imagem = username + '.' + image.name.split('.')[1]
            FileSystemStorage().save('images/utilizador/' + nome_imagem, image)
            utilizador = Utilizador(user=user, nome_imagem=nome_imagem)
            utilizador.save()
            return HttpResponseRedirect(reverse('ibuy:index'))
    else:
        context = {'form': ContaForm}
        return render(request, 'ibuy/criarconta.html', context)


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


def perfil(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    utilizador = user.utilizador
    context = {
        'user': user,
        'utilizador': utilizador,
    }
    return render(request, 'ibuy/perfil.html', context)


def produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    user = get_object_or_404(User, pk=produto.user_id)
    listacomentarios = Comentario.objects.filter(produto_id=produto_id)
    context = {
        'listacomentarios': listacomentarios,
        'nome_user': user.username,
        'produto': produto,
        'form': ComprarProdutoForm,
        'comentarioform': ComentarioForm,
    }
    return render(request, 'ibuy/produto.html', context)


def likeProduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    produto.likes.add(request.user)
    return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))

def adicionarcomentario(request, produto_id):
    if request.method == 'POST':
        print("entrei no post")
        texto = request.POST['texto']
        produto = get_object_or_404(Produto, pk=produto_id)
        comentario = Comentario(user=request.user, produto=produto, texto=texto)
        comentario.save()
        print(comentario.texto)
        return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))


# fazer com que o utilizador tambem possa incrementar a quantidade no carrinho
def carrinho(request):
    if 'carrinho' in request.session and request.session['carrinho']:
        lista = request.session['carrinho']
        lista_carrinho_nova = []

        for i in lista:
            produto_id = i[0]
            produto = get_object_or_404(Produto, pk=produto_id)
            quantidade = i[1]
            item = (produto, quantidade)
            lista_carrinho_nova.append(item)

        context = {
            'lista': lista_carrinho_nova,
            'form': ComprarProdutoForm
        }

        return render(request, 'ibuy/carrinho.html', context)
    else:
        return render(request, 'ibuy/carrinho.html')


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def meusprodutos(request):
    lista_produtos = Produto.objects.filter(user_id=request.user.id)
    context = {'lista_produtos': lista_produtos}
    return render(request, 'ibuy/meusprodutos.html', context)


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def criarproduto(request):
    # form = ProdutoForm()
    if request.method == 'POST':
        # form = ProdutoForm(request.POST)
        # if form.is_valid():
        #   form.save()
        #  return HttpResponseRedirect(reverse('ibuy:meusprodutos'))
        nome = request.POST['nome']
        quantidade = request.POST['quantidade']
        preco = request.POST['preco']
        descricao = request.POST['descricao']
        condicao = request.POST['condicao']
        # imagem = request.FILES['myfile']
        # FileSystemStorage().save(imagem.name, imagem)
        categoria_id = request.POST['categoria']
        image = request.FILES['img_produto']
        categoria = get_object_or_404(Categoria, pk=categoria_id)

        # print(produto.user)
        if not (nome and quantidade and preco and descricao and condicao and image and categoria):
            return render(request, 'ibuy/criarproduto.html',
                          {'form': ProdutoForm, 'error_message': "Não preencheu todos os campos!"})

        produto = Produto(nome=nome, quantidade=quantidade, preco=preco, descricao=descricao,
                          condicao=condicao, categoria=categoria, user=request.user)
        produto.save()
        nome_imagem = str(produto.id) + '.' + image.name.split('.')[1]
        FileSystemStorage().save('images/produto/' + nome_imagem, image)
        produto.imagem = nome_imagem
        produto.save()

        return HttpResponseRedirect(reverse('ibuy:meusprodutos'))
    else:
        # form = ProdutoForm
        # context = {
        #   "form":form
        # }
        # return render(request, 'ibuy/criarproduto.html', context)

        context = {}
        context['form'] = ProdutoForm
        return render(request, 'ibuy/criarproduto.html', context)


def apagarproduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    produto.delete()
    return HttpResponseRedirect(reverse('ibuy:meusprodutos'))


# adiciona um produto ao carrinho / se o user der log out, a informaçao do carrinho desparece
def updatecarrinho(request, produto_id):
    if request.method == 'POST':
        quantidade = request.POST['quantidade']
        produto = get_object_or_404(Produto, pk=produto_id)

        # se for escolhido uma quantidade superiror à do produto ou nao for um num inteiro positivo
        if produto.quantidade < int(quantidade) or int(quantidade) <= 0:
            # enviar mensagem de erro
            print("quantidade invalida")
            return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))

        # no caso de adicionar o primeiro produto ao carrinho
        if not 'carrinho' in request.session or not request.session['carrinho']:
            print("criei primeira vez")
            item = (produto_id, quantidade)
            request.session['carrinho'] = [item]
            return HttpResponseRedirect(reverse('ibuy:carrinho'))

        # no caso de adicionar mais produtos

        lista_carrinho = request.session['carrinho']
        item = (produto_id, quantidade)

        for i in range(len(lista_carrinho)):

            # se ja existir o produto no carrinho
            if (lista_carrinho[i][0] == item[0]):
                print("antes")
                print(lista_carrinho[i])
                lista_carrinho[i] = (item[0],int(quantidade))
                print("depois")
                print(lista_carrinho[i])
                request.session['carrinho'] = lista_carrinho
                return HttpResponseRedirect(reverse('ibuy:carrinho'))

            # se nao existir
            else:
                lista_carrinho.append(item)
                request.session['carrinho'] = lista_carrinho
                return HttpResponseRedirect(reverse('ibuy:carrinho'))




# remove um produto do carrinho
def removercarrinho(request, produto_id):
    if 'carrinho' in request.session and request.session['carrinho']:
        lista_carrinho = request.session['carrinho']
        for item in lista_carrinho:
            if int(item[0]) == produto_id:
                lista_carrinho.remove(item)
                request.session['carrinho'] = lista_carrinho
        return HttpResponseRedirect(reverse('ibuy:carrinho'))

# session[carrinho] = lista
# lista = {
#   (produto_id, quantidade)
# }
