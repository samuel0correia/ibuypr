from idlelib import window

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import Utilizador, Produto, Categoria, Comentario, HistoricoCompras
from .forms import ProdutoForm, ComprarProdutoForm, ContaForm, ComentarioForm, UserForm, UtilizadorForm, PasswordForm
import datetime


def is_admin(user):
    if user.is_superuser:
        return True
    return False


def is_user(user):
    return not is_admin(user)


def index(request):
    titulo = "Todas as Categorias"
    lista_produtos = Produto.objects.exclude(user_id=request.user.id)
    if request.method == 'GET':
        if request.GET.get('categoria', False):
            categoria = request.GET['categoria']
            if categoria != "Tudo":
                titulo = "Categoria: " + categoria
                categoria_id = Categoria.objects.get(tipo=categoria).pk
                lista_produtos = Produto.objects.exclude(user_id=request.user.id).filter(categoria=categoria_id)
            else:
                titulo = "Todas as Categorias"
                lista_produtos = Produto.objects.exclude(user_id=request.user.id)
        elif request.GET.get('pesquisa', False):
            texto_pesquisa = request.GET['pesquisa']
            titulo = "Todos os resultados para: " + texto_pesquisa
            lista_produtos = Produto.objects.exclude(user_id=request.user.id).filter(nome__icontains=texto_pesquisa)
    lista_produtos = sorted(lista_produtos, key=lambda x: x.total_likes(), reverse=True)  # ordenar por likes
    context = {'lista_produtos': lista_produtos, 'titulo': titulo}
    return render(request, 'ibuy/index.html', context)


def ondeestamos(request):
    return render(request, 'ibuy/ondeestamos.html')


# mudar / melhorar
def criarconta(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        image = request.FILES.get('img_produto', False)
        if not (first_name and last_name and username and password):
            return render(request, 'ibuy/criarconta.html',
                          {'form': ContaForm, 'error_message': "Não preencheu todos os campos!"})
        if password != cpassword:
            return render(request, 'ibuy/criarconta.html',
                          {'form': ContaForm, 'error_message': "As passwords inseridas não são iguais!"})
        if User.objects.filter(username=username).exists():
            return render(request, 'ibuy/criarconta.html',
                          {'form': ContaForm, 'error_message': "Já existe uma conta com esse username associado"})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            utilizador = Utilizador(user=user)
            if image:
                nome_imagem = username + '.' + image.name.split('.')[1]
                FileSystemStorage().save('images/utilizador/' + nome_imagem, image)
                utilizador.imagem = nome_imagem
            utilizador.save()
            return HttpResponseRedirect(reverse('ibuy:index'))
    else:
        context = {
            'user_form': UserForm,
            'utilizador_form': UtilizadorForm,
            'password_form': PasswordForm
        }
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
    user = get_object_or_404(User, pk=request.user.id)
    user_form = UserForm(instance=user)
    context = {
        'user_form': user_form,
        'utilizador_form': UtilizadorForm,
        'password_form': PasswordForm,
    }
    return render(request, 'ibuy/minhaconta.html', context)


def alterarpassword(request):
    user = get_object_or_404(User, pk=request.user.id)
    user_form = UserForm(instance=user)
    if request.method == 'POST':
        passwordatual = request.POST['passwordatual']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if not (passwordatual and password and cpassword):
            return render(request, 'ibuy/minhaconta.html',
                          {'user_form': user_form, 'utilizador_form': UtilizadorForm, 'password_form': PasswordForm,
                           'error_message': "Não preencheu todos os campos!"})
        if password != cpassword:
            return render(request, 'ibuy/minhaconta.html',
                          {'user_form': user_form, 'utilizador_form': UtilizadorForm, 'password_form': PasswordForm,
                           'error_message': "As passwords inseridas não são iguais!"})
        if not user.check_password(passwordatual):
            return render(request, 'ibuy/minhaconta.html',
                          {'user_form': user_form, 'utilizador_form': UtilizadorForm, 'password_form': PasswordForm,
                           'error_message': "A password atual inserida está errada!"})
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(reverse('ibuy:index'))
    else:
        return minhaconta(request)


def alterarconta(request):
    user = get_object_or_404(User, pk=request.user.id)
    user_form = UserForm(instance=user)
    context = {  # adicionar este onde necessário
        'user_form': user_form,
        'utilizador_form': UtilizadorForm,
        'password_form': PasswordForm,
    }
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        image = request.FILES.get('img_produto', False)
        if not (first_name and last_name and username and email):
            return render(request, 'ibuy/minhaconta.html',
                          {'user_form': user_form, 'utilizador_form': UtilizadorForm, 'password_form': PasswordForm,
                           'error_message': "Não preencheu todos os campos!"})
        if User.objects.filter(username=username).exists() and username != user.username:
            return render(request, 'ibuy/minhaconta.html',
                          {'user_form': user_form, 'utilizador_form': UtilizadorForm, 'password_form': PasswordForm,
                           'error_message': "Já existe uma conta com esse username associado"})
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            if image:
                FileSystemStorage().delete('images/utilizador/' + user.utilizador.imagem)
                nome_imagem = str(user.id) + '.' + image.name.split('.')[1]
                FileSystemStorage().save('images/utilizador/' + nome_imagem, image)
                user.utilizador.imagem = nome_imagem
                user.utilizador.save()
        return HttpResponseRedirect(reverse('ibuy:index'))
    else:
        return minhaconta(request)


def perfil(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    lista_produtos = Produto.objects.filter(user_id=user.id)
    context = {
        'user': user,
        'lista_produtos': lista_produtos
    }
    return render(request, 'ibuy/perfil.html', context)


def produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    user = get_object_or_404(User, pk=produto.user_id)
    listacomentarios = Comentario.objects.filter(produto_id=produto_id)
    liked = produto.likes.filter(id=request.user.id).exists()
    context = {
        'listacomentarios': listacomentarios,
        'nome_user': user.username,
        'produto': produto,
        'form': ComprarProdutoForm,
        'comentarioform': ComentarioForm,
        'liked': liked,
    }
    return render(request, 'ibuy/produto.html', context)


@user_passes_test(is_user, login_url=reverse_lazy('ibuy:loginuser'))
def likeProduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if produto.likes.filter(id=request.user.id).exists():
        produto.likes.remove(request.user)
        # liked = False
    else:
        produto.likes.add(request.user)
        # liked = True
    return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))


@user_passes_test(is_user, login_url=reverse_lazy('ibuy:loginuser'))
def adicionarcomentario(request, produto_id):
    if request.method == 'POST':
        texto = request.POST['texto']
        produto = get_object_or_404(Produto, pk=produto_id)
        comentario = Comentario(user=request.user, produto=produto, texto=texto)
        comentario.save()
        return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))


# fazer com que o utilizador tambem possa incrementar a quantidade no carrinho
# organizar o codigo melhor, se possivel
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:loginuser'))
def carrinho(request):
    #user = get_object_or_404(User, pk=request.user.id)
    #utilizador = user.utilizador
    if 'carrinho' in request.session and request.session['carrinho']:
        quantidadetotal = 0
        precototal = 0
        lista = request.session['carrinho']
        lista_carrinho_nova = []

        for i in lista:
            produto_id = i[0]
            produto = get_object_or_404(Produto, pk=produto_id)
            quantidade = i[1]
            quantidadetotal = quantidadetotal + int(quantidade)
            precototal = precototal + produto.preco * int(quantidade)
            item = (produto, quantidade)
            lista_carrinho_nova.append(item)

        request.session['precototal'] = int(precototal)

        context = {
            'lista': lista_carrinho_nova,
            'form': ComprarProdutoForm,
            'quantidadetotal': quantidadetotal,
            'precototal': precototal,
            #'balancocredito': utilizador.total_credito(),
        }
        return render(request, 'ibuy/carrinho.html', context)
    else:
        return render(request, 'ibuy/carrinho.html')


def efetuarcompra(request):
    user = get_object_or_404(User, pk=request.user.id)
    utilizador = user.utilizador

    if 'carrinho' in request.session and request.session['carrinho']:
        precototal = request.session['precototal']
        lista = request.session['carrinho']

        if utilizador.credito < precototal:
            print("nao tem dinheiro")
            return HttpResponseRedirect(reverse('ibuy:carrinho'))
        else:
            for i in lista:
                produto_id = i[0]
                produto = get_object_or_404(Produto, pk=produto_id)
                quantidade = i[1]

                historico = HistoricoCompras(user=user, produto=produto, quantidade=quantidade, timestamp = datetime.datetime.now())
                historico.save()

                produto.quantidade = produto.quantidade - int(quantidade)
                produto.save()

                vendedor = get_object_or_404(Utilizador, user_id=produto.user.id)
                vendedor.adicionar_credito(produto.preco*int(quantidade))


            utilizador.remover_credito(precototal)
            del request.session['carrinho']
            return HttpResponseRedirect(reverse('ibuy:carrinho'))  # talvez reencaminhar para outro sitio


def adicionarcredito(request):
    user = get_object_or_404(User, pk=request.user.id)
    utilizador = user.utilizador
    utilizador.adicionar_credito(100)
    return HttpResponseRedirect(reverse('ibuy:adicionarmoeda'))


@user_passes_test(is_user, login_url=reverse_lazy('ibuy:loginuser'))
def meusprodutos(request):
    lista_produtos = Produto.objects.filter(user_id=request.user.id)
    context = {'lista_produtos': lista_produtos}
    return render(request, 'ibuy/meusprodutos.html', context)


@user_passes_test(is_user, login_url=reverse_lazy('ibuy:loginuser'))
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
        categoria_id = request.POST['categoria']
        image = request.FILES.get('img_produto', False)
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        if not (nome and quantidade and preco and descricao and condicao and categoria):
            return render(request, 'ibuy/criarproduto.html',
                          {'form': ProdutoForm, 'error_message': "Não preencheu todos os campos!"})

        produto = Produto(nome=nome, quantidade=quantidade, preco=preco, descricao=descricao,
                          condicao=condicao, categoria=categoria, user=request.user)
        produto.save()

        if image:
            nome_imagem = str(produto.id) + '.' + image.name.split('.')[1]
            FileSystemStorage().save('images/produto/' + nome_imagem, image)
            produto.imagem = nome_imagem
            produto.save()

        return HttpResponseRedirect(reverse('ibuy:meusprodutos'))
    else:
        context = {
            'form': ProdutoForm,
        }
        return render(request, 'ibuy/criarproduto.html', context)


# verificação para ver se o produto pertence ao utilizador logado
@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def apagarproduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    FileSystemStorage().delete('images/produto/' + produto.imagem)
    produto.delete()
    return HttpResponseRedirect(reverse('ibuy:meusprodutos'))


# atualiza as quantidades na pagina do carrinho
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:loginuser'))
def updatequantidade(request, produto_id):
    if request.method == 'POST':
        quantidade = request.POST['quantidade']
        produto = get_object_or_404(Produto, pk=produto_id)

        # se for escolhido uma quantidade superiror à do produto ou nao for um num inteiro positivo
        if produto.quantidade < int(quantidade) or int(quantidade) < 0:
            # enviar mensagem de erro
            return HttpResponseRedirect(reverse('ibuy:carrinho'))

        if 'carrinho' in request.session and request.session['carrinho']:
            lista_carrinho = request.session['carrinho']
            item = (produto_id, quantidade)

            for i in range(len(lista_carrinho)):
                if lista_carrinho[i][0] == item[0]:
                    if int(quantidade) == 0:
                        lista_carrinho.remove(lista_carrinho[i])
                        request.session['carrinho'] = lista_carrinho
                        return HttpResponseRedirect(reverse('ibuy:carrinho'))
                    else:
                        lista_carrinho[i] = (item[0], int(quantidade))
                        request.session['carrinho'] = lista_carrinho
                        return HttpResponseRedirect(reverse('ibuy:carrinho'))


# adiciona um produto ao carrinho / se o user der log out, a informaçao do carrinho desparece
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:loginuser'))
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

            # Se ja existir o produto no carrinho soma à quantidade existente
            if (lista_carrinho[i][0] == item[0]):
                # Se a quantidade futura for maior do que o possivel nao da
                if int(lista_carrinho[i][1]) + int(quantidade) <= produto.quantidade:
                    print("vou adicionar")
                    print(int(lista_carrinho[i][1]))
                    lista_carrinho[i] = (item[0], int(lista_carrinho[i][1]) + int(quantidade))
                    request.session['carrinho'] = lista_carrinho
                    return HttpResponseRedirect(reverse('ibuy:carrinho'))
                else:
                    print("impossivel")
                    print(int(item[1]) + int(quantidade))
                    return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))
            # se nao existir
            else:
                lista_carrinho.append(item)
                request.session['carrinho'] = lista_carrinho
                return HttpResponseRedirect(reverse('ibuy:carrinho'))


# remove um produto do carrinho
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:loginuser'))
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


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
# verificação para ver se o produto pertence ao utilizador logado
def alterarproduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.user.id == produto.user.id or request.user.is_superuser:
        if request.method == 'POST':
            nome = request.POST['nome']
            quantidade = request.POST['quantidade']
            preco = request.POST['preco']
            descricao = request.POST['descricao']
            condicao = request.POST['condicao']
            categoria_id = request.POST['categoria']
            categoria = get_object_or_404(Categoria, pk=categoria_id)
            image = request.FILES.get('img_produto', False)

            if not (nome and quantidade and preco and descricao and condicao and categoria):
                return render(request, 'ibuy/alterarproduto.html',
                              {'form': ProdutoForm, 'error_message': "Não preencheu todos os campos!"})

            produto = get_object_or_404(Produto, pk=produto_id)
            produto.nome = nome
            produto.quantidade = quantidade
            produto.preco = preco
            produto.descricao = descricao
            produto.condicao = condicao
            produto.categoria = categoria

            if image:
                FileSystemStorage().delete('images/produto/' + produto.imagem)
                nome_imagem = str(produto.id) + '.' + image.name.split('.')[1]
                FileSystemStorage().save('images/produto/' + nome_imagem, image)
                produto.imagem = nome_imagem
            produto.save()
            return HttpResponseRedirect(reverse('ibuy:meusprodutos'))
        else:
            produto = get_object_or_404(Produto, pk=produto_id)
            form = ProdutoForm(instance=produto)
            context = {
                'produto': produto,
                'form': form,
            }
            return render(request, 'ibuy/alterarproduto.html', context)
    else:
        return loginuser(request)


@user_passes_test(is_admin, login_url=reverse_lazy('ibuy:loginuser'))
def utilizadores(request):
    lista_users = User.objects.filter(is_superuser=0)  # ver pelo tipo user do utilizador talvez
    context = {'lista_users': lista_users}
    return render(request, 'ibuy/utilizadores.html', context)


@user_passes_test(is_admin, login_url=reverse_lazy('ibuy:loginuser'))
def apagarutilizador(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    FileSystemStorage().delete('images/utilizador/' + user.imagem)
    user.utilizador.delete()
    user.delete()
    return utilizadores(request)


def historiaempresa(request):
    return render(request, 'ibuy/historiaempresa.html')


def adicionarmoeda(request):
    return render(request, 'ibuy/adicionarmoeda.html')
