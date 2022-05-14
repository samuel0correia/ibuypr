from django.urls import include, path
from . import views

# (. significa que importa views da mesma directoria)

app_name = 'ibuy'
urlpatterns = [
    path('', views.index, name='index'),

    # Login, Conta e Perfil
    # path('loginview', views.loginview, name='loginview'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('logoutview', views.logoutview, name='logoutview'),
    path('criarconta', views.criarconta, name='criarconta'),
    path('minhaconta/<int:user_id>', views.minhaconta, name='minhaconta'),
    path('alterarconta/<int:user_id>', views.alterarconta, name='alterarconta'),
    path('alterarpassword/<int:user_id>', views.alterarpassword, name='alterarpassword'),
    path('perfil/<int:user_id>', views.perfil, name='perfil'),

    # Produtos
    path('criarproduto', views.criarproduto, name='criarproduto'),
    path('meusprodutos', views.meusprodutos, name='meusprodutos'),
    path('carrinho', views.carrinho, name='carrinho'),
    path('produto/<int:produto_id>', views.produtoview, name='produto'),
    path('produto/<int:produto_id>/alterarproduto', views.alterarproduto, name='alterarproduto'),
    path('produto/<int:produto_id>/apagarproduto', views.apagarproduto, name='apagarproduto'),
    path('produto/<int:produto_id>/like', views.likeproduto, name='like_produto'),
    path('updatecarrinho/<int:produto_id>', views.updatecarrinho, name='updatecarrinho'),
    path('updatequantidade/<int:produto_id>', views.updatequantidade, name='updatequantidade'),
    path('adicionarcomentario/<int:produto_id>', views.adicionarcomentario, name='adicionarcomentario'),
    path('removercarrinho/<int:produto_id>', views.removercarrinho, name='removercarrinho'),
    path('adicionarcredito', views.adicionarcredito, name='adicionarcredito'),
    path('efetuarcompra', views.efetuarcompra, name='efetuarcompra'),
    # Geral
    path('historiaempresa', views.historiaempresa, name='historiaempresa'),
    path('ondeestamos', views.ondeestamos, name='ondeestamos'),
    path('adicionarmoeda', views.adicionarmoeda, name='adicionarmoeda'),



    path('erro', views.erro, name='erro'),
    # Admin
    path('utilizadores', views.utilizadores, name='utilizadores'),
    path('apagarutilizador/<int:user_id>', views.apagarutilizador, name='apagarutilizador')

]
