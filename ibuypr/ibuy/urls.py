from django.urls import include, path
from . import views
# (. significa que importa views da mesma directoria)

app_name = 'ibuy'
urlpatterns = [
    path('', views.index, name='index'),

    # Login, Conta e Perfil
    #path('loginview', views.loginview, name='loginview'),
    #path('login', views.loginpage, name='loginpage'),
    #path('logoutview', views.logoutview, name='logoutview'),
    #path('criarconta', views.criarconta, name='criarconta'),
    path('minhaconta', views.minhaconta, name='minhaconta'),
    #path('<str:username>', views.perfil, name='perfil'),

    # Produtos
    #path('criarproduto', views.criarproduto, name='criarproduto'),
    #path('meusprodutos', views.meusprodutos, name='meusprodutos'),
    #path('carrinho', views.carrinho, name='carrinho'),
    #path('<int:produto_id>', views.produto, name='produto'),

    # Geral
    #path('error', views.error, name='error'),

]