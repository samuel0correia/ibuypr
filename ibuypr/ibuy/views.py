from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import Utilizador, Produto, Categoria, Comentario, HistoricoCompras
from .forms import ProdutoForm, ComentarioForm, UserForm, UtilizadorForm, PasswordForm
from datetime import datetime
from django.core.paginator import Paginator
from decimal import Decimal


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
    lista_produtos = list(filter(lambda x: x.quantidade != 0, lista_produtos))  # remover produtos com 0 unidades
    if not lista_produtos:
        titulo = "Não existem produtos à venda"

    paginas = Paginator(lista_produtos, 6)
    page_number = request.GET.get('page')
    page_obj = paginas.get_page(page_number)

    context = {'lista_produtos': lista_produtos, 'titulo': titulo,
               'page_obj': page_obj
               }
    return render(request, 'ibuy/index.html', context)


def ondeestamos(request):
    return render(request, 'ibuy/ondeestamos.html')


def criarconta(request):
    context = {
        'user_form': UserForm,
        'utilizador_form': UtilizadorForm,
        'password_form': PasswordForm
    }
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        image = request.FILES.get('img_utilizador', False)
        if not (first_name and last_name and username and password):
            context['error_message'] = "Não preencheu todos os campos!"
            return render(request, 'ibuy/criarconta.html', context)
        if password != cpassword:
            context['error_message'] = "As passwords inseridas não são iguais!"
            return render(request, 'ibuy/criarconta.html', context)
        if User.objects.filter(username=username).exists():
            context['error_message'] = "Já existe uma conta com esse username associado"
            return render(request, 'ibuy/criarconta.html', context)
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
            return HttpResponseRedirect(reverse('ibuy:loginuser'))
    else:
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
            return render(request, 'ibuy/loginuser.html', {'error_message': "Username/Password inválidos!"})
    else:
        return render(request, 'ibuy/loginuser.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('ibuy:index'))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def minhaconta(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not (request.user.is_superuser or user.id == request.user.id):
        return render(request, 'ibuy/erro.html')
    user_form = UserForm(instance=user)
    context = {
        'user': user,
        'user_form': user_form,
        'utilizador_form': UtilizadorForm,
        'password_form': PasswordForm,
    }
    return render(request, 'ibuy/minhaconta.html ', context)


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def alterarpassword(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not (request.user.is_superuser or user.id == request.user.id):
        return render(request, 'ibuy/erro.html')
    user_form = UserForm(instance=user)
    context = {
        'user': user,
        'user_form': user_form,
        'utilizador_form': UtilizadorForm,
        'password_form': PasswordForm,
    }
    if request.method == 'POST':
        passwordatual = request.POST['passwordatual']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if not (passwordatual and password and cpassword):
            context['error_message'] = "Não preencheu todos os campos!"
            return render(request, 'ibuy/minhaconta.html', context)
        if password != cpassword:
            context['error_message'] = "As passwords inseridas não são iguais!"
            return render(request, 'ibuy/minhaconta.html', context)
        if not user.check_password(passwordatual):
            context['error_message'] = "A password atual inserida está errada!"
            return render(request, 'ibuy/minhaconta.html', context)
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(reverse('ibuy:index'))
    else:
        return HttpResponseRedirect(reverse('ibuy:minhaconta', args=(user.id,)))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def alterarconta(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not (request.user.is_superuser or user.id == request.user.id):
        return render(request, 'ibuy/erro.html')
    user_form = UserForm(instance=user)
    context = {
        'user': user,
        'user_form': user_form,
        'utilizador_form': UtilizadorForm,
        'password_form': PasswordForm,
    }
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        image = request.FILES.get('img_utilizador', False)
        if not (first_name and last_name and username and email):
            context['error_message'] = "Não preencheu todos os campos!"
            return render(request, 'ibuy/minhaconta.html', context)
        if User.objects.filter(username=username).exists() and username != user.username:
            context['error_message'] = "Já existe uma conta com esse username associado"
            return render(request, 'ibuy/minhaconta.html', context)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if image:
            if not user.utilizador.imagem == 'utilizador.png':
                FileSystemStorage().delete('images/utilizador/' + user.utilizador.imagem)
            nome_imagem = str(user.id) + '.' + image.name.split('.')[1]
            FileSystemStorage().save('images/utilizador/' + nome_imagem, image)
            user.utilizador.imagem = nome_imagem
            user.utilizador.save()
        return HttpResponseRedirect(reverse('ibuy:index'))
    else:
        return minhaconta(request, user.id)


def perfil(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser and request.user.id != user.id:
        return HttpResponseRedirect(reverse('ibuy:erro'))
    lista_produtos = Produto.objects.filter(user_id=user.id)
    lista_produtos = sorted(lista_produtos, key=lambda x: x.total_likes(), reverse=True)  # ordenar por likes
    if user.id != request.user.id:
        lista_produtos = list(filter(lambda x: x.quantidade != 0, lista_produtos))  # remover produtos com 0 unidades

    paginas = Paginator(lista_produtos, 4)
    page_number = request.GET.get('page')
    page_obj = paginas.get_page(page_number)
    context = {
        'user': user,
        'lista_produtos': lista_produtos,
        'page_obj': page_obj,
    }
    return render(request, 'ibuy/perfil.html', context)


def produto(request, produto_id):
    p = get_object_or_404(Produto, pk=produto_id)
    user = get_object_or_404(User, pk=p.user_id)
    listacomentarios = Comentario.objects.filter(produto_id=produto_id).order_by('-timestamp')
    liked = p.likes.filter(id=request.user.id).exists()
    context = {
        'listacomentarios': listacomentarios,
        'nome_user': user.username,
        'produto': p,
        'comentarioform': ComentarioForm,
        'liked': liked,
    }
    return render(request, 'ibuy/produto.html', context)


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def likeproduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if produto.likes.filter(id=request.user.id).exists():
        produto.likes.remove(request.user)
    else:
        produto.likes.add(request.user)
    return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def adicionarcomentario(request, produto_id):
    if request.method == 'POST':
        texto = request.POST['texto']
        produto = get_object_or_404(Produto, pk=produto_id)
        comentario = Comentario(user=request.user, produto=produto, texto=texto, timestamp=datetime.now())
        comentario.save()
        return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))


def apagarcomentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    produto = get_object_or_404(Produto, pk=comentario.produto.id)
    if comentario.user.id == request.user.id or request.user.is_superuser:
        comentario.delete()
        return HttpResponseRedirect(reverse('ibuy:produto', args=(produto.id,)))
    else:
        return HttpResponseRedirect(reverse('ibuy:produto', args=(produto.id,)))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def carrinho(request):
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

        request.session['precototal'] = str(precototal)
        request.session['quantidadetotal'] = int(quantidadetotal)

        context = {
            'lista': lista_carrinho_nova,
        }
        return render(request, 'ibuy/carrinho.html', context)
    else:
        return render(request, 'ibuy/carrinho.html')


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def efetuarcompra(request):
    user = get_object_or_404(User, pk=request.user.id)
    utilizador = user.utilizador

    if 'carrinho' in request.session and request.session['carrinho']:
        precototal = Decimal(request.session['precototal'])
        lista = request.session['carrinho']

        if utilizador.credito < precototal:
            return HttpResponseRedirect(reverse('ibuy:adicionarmoeda'))
        else:
            for i in lista:
                produto_id = i[0]
                produto = get_object_or_404(Produto, pk=produto_id)
                quantidade = i[1]

                historico = HistoricoCompras(user=user, produto=produto, quantidade=quantidade,
                                             timestamp=datetime.now())
                historico.save()

                produto.quantidade = produto.quantidade - int(quantidade)
                produto.save()

                vendedor = get_object_or_404(Utilizador, user_id=produto.user.id)
                if vendedor.total_credito() + Decimal(produto.preco) * Decimal(quantidade) > 9999.99:
                    vendedor.credito = 9999.99
                    vendedor.save()
                else:
                    vendedor.adicionar_credito(Decimal(produto.preco) * Decimal(quantidade))

            utilizador.remover_credito(precototal)
            del request.session['carrinho']
            return HttpResponseRedirect(reverse('ibuy:index'))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def meusprodutos(request):
    lista_produtos = list(Produto.objects.filter(user_id=request.user.id))
    lista_produtos = sorted(lista_produtos, key=lambda x: x.total_likes(), reverse=True)
    paginas = Paginator(lista_produtos, 6)
    page_number = request.GET.get('page')
    page_obj = paginas.get_page(page_number)
    context = {
        'lista_produtos': lista_produtos,
        'page_obj': page_obj,
    }
    return render(request, 'ibuy/meusprodutos.html', context)


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def criarproduto(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        quantidade = request.POST['quantidade']
        preco = request.POST['preco']
        descricao = request.POST['descricao']
        condicao = request.POST['condicao']
        categoria_id = request.POST['categoria']
        video_embed = request.POST['video_embed']
        image = request.FILES.get('imagem', False)
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        if not (nome and quantidade and preco and descricao and condicao and categoria):
            return render(request, 'ibuy/criarproduto.html',
                          {'form': ProdutoForm, 'error_message': "Não preencheu todos os campos!"})

        produto = Produto(nome=nome, quantidade=quantidade, preco=preco, descricao=descricao,
                          condicao=condicao, categoria=categoria, user=request.user, video_embed=video_embed,
                          timestamp=datetime.now())
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


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def apagarproduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if not (request.user.is_superuser or request.user.id == produto.user_id):
        return render(request, 'ibuy/erro.html')

    if not produto.imagem == 'produto.png':
        FileSystemStorage().delete('images/produto/' + produto.imagem)
    produto.delete()
    return HttpResponseRedirect(reverse('ibuy:meusprodutos'))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def updatequantidade(request, produto_id):
    if request.method == 'POST':
        quantidade = request.POST['quantidade']
        produto = get_object_or_404(Produto, pk=produto_id)

        if produto.quantidade < int(quantidade) or int(quantidade) < 0:
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


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def updatecarrinho(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.user.id == produto.user_id:
        return render(request, 'ibuy/erro.html')

    if request.method == 'POST':
        quantidade = request.POST['quantidade']

        if produto.quantidade < int(quantidade) or int(quantidade) <= 0:
            return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))

        if not 'carrinho' in request.session or not request.session['carrinho']:
            item = (produto_id, quantidade)
            request.session['carrinho'] = [item]
            return HttpResponseRedirect(reverse('ibuy:carrinho'))

        lista_carrinho = request.session['carrinho']
        item = (produto_id, quantidade)

        for i in range(len(lista_carrinho)):

            if lista_carrinho[i][0] == item[0]:

                if int(lista_carrinho[i][1]) + int(quantidade) <= produto.quantidade:
                    lista_carrinho[i] = (item[0], int(lista_carrinho[i][1]) + int(quantidade))
                    request.session['carrinho'] = lista_carrinho
                    return HttpResponseRedirect(reverse('ibuy:carrinho'))
                else:
                    lista_carrinho[i] = (item[0], produto.quantidade)
                    request.session['carrinho'] = lista_carrinho
                    return HttpResponseRedirect(reverse('ibuy:carrinho'))
            else:
                lista_carrinho.append(item)
                request.session['carrinho'] = lista_carrinho
                return HttpResponseRedirect(reverse('ibuy:carrinho'))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_user, login_url=reverse_lazy('ibuy:erro'))
def removercarrinho(request, produto_id):
    if 'carrinho' in request.session and request.session['carrinho']:
        lista_carrinho = request.session['carrinho']
        for item in lista_carrinho:
            if int(item[0]) == produto_id:
                lista_carrinho.remove(item)
                request.session['carrinho'] = lista_carrinho
        return HttpResponseRedirect(reverse('ibuy:carrinho'))


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def alterarproduto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if not (request.user.is_superuser or request.user.id == produto.user_id):
        return render(request, 'ibuy/erro.html')
    if request.method == 'POST':
        nome = request.POST['nome']
        quantidade = request.POST['quantidade']
        preco = request.POST['preco']
        descricao = request.POST['descricao']
        condicao = request.POST['condicao']
        categoria_id = request.POST['categoria']
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        image = request.FILES.get('imagem', False)
        video_embed = request.POST['video_embed']

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
        produto.video_embed = video_embed

        if image:
            if not produto.imagem == 'produto.png':
                FileSystemStorage().delete('images/produto/' + produto.imagem)
            nome_imagem = str(produto.id) + '.' + image.name.split('.')[1]
            FileSystemStorage().save('images/produto/' + nome_imagem, image)
            produto.imagem = nome_imagem
        produto.save()
        return HttpResponseRedirect(reverse('ibuy:produto', args=(produto_id,)))
    else:
        produto = get_object_or_404(Produto, pk=produto_id)
        form = ProdutoForm(instance=produto)
        context = {
            'produto': produto,
            'form': form,
        }
        return render(request, 'ibuy/alterarproduto.html', context)


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_admin, login_url=reverse_lazy('ibuy:erro'))
def utilizadores(request):
    lista_users = list(User.objects.filter(is_superuser=0))  # ver pelo tipo user do utilizador talvez
    paginas = Paginator(lista_users, 6)
    page_number = request.GET.get('page')
    page_obj = paginas.get_page(page_number)
    context = {
        'lista_users': lista_users,
        'page_obj': page_obj,
    }
    return render(request, 'ibuy/utilizadores.html', context)


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
@user_passes_test(is_admin, login_url=reverse_lazy('ibuy:erro'))
def apagarutilizador(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not user.utilizador.imagem == 'utilizador.png':
        FileSystemStorage().delete('images/utilizador/' + user.utilizador.imagem)
    user.utilizador.delete()
    user.delete()
    return HttpResponseRedirect(reverse('ibuy:utilizadores'))


def erro(request):
    return render(request, 'ibuy/erro.html')


def historiaempresa(request):
    return render(request, 'ibuy/historiaempresa.html')


def ondeestamos(request):
    return render(request, 'ibuy/ondeestamos.html')


def nossamoeda(request):
    return render(request, 'ibuy/nossamoeda.html')


@login_required(login_url=reverse_lazy('ibuy:loginuser'))
def adicionarcredito(request):
    if request.method == 'POST':
        quantidadecredito = Decimal(request.POST['quantidade'])
        user = get_object_or_404(User, pk=request.user.id)
        utilizador = user.utilizador
        if utilizador.total_credito() + quantidadecredito > 9999.99:
            utilizador.credito = 9999.99
            utilizador.save()
        else:
            utilizador.adicionar_credito(quantidadecredito)
        return render(request, 'ibuy/adicionarcredito.html')
    else:
        return render(request, 'ibuy/adicionarcredito.html')
