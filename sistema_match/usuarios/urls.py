from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.login, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('plataforma/', views.plataforma, name='plataforma'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('filmes/', views.filmes, name='filmes'),
    path('series/', views.series, name='series'),
    path('animacoes/', views.animacoes, name='animacoes'),
    path('livros/', views.livros, name='livros'),
    path('search_profiles/', views.search_profiles, name='search_profiles'), 
    path('upload-image/', views.upload_image, name='upload_image'),
    path('filme_usuario/', views.filme_usuario, name='filme_usuario'),
    path('deletar_filme/<int:filme_id>/', views.deletar_filme, name='deletar_filme'),
    path('livro_usuario/', views.livro_usuario, name='livro_usuario'),
    path('deletar_livro/<int:livro_id>/', views.deletar_livro, name='deletar_livro'),
    path('serie_usuario/', views.serie_usuario, name='serie_usuario'),
    path('deletar_serie/<int:serie_id>/', views.deletar_serie, name='deletar_serie'),
    path('animacao_usuario/', views.animacao_usuario, name='animacao_usuario'),
    path('deletar_animacao/<int:animacao_id>/', views.deletar_animacao, name='deletar_animacao'),
    path('profile_usuario/', views.profile_usuario, name='profile_usuario'),
    path('profile_usuario/<int:user_id>/', views.profile_usuario, name='profile_usuario'),
    path('outros_perfis/<int:user_id>/', views.outros_perfis, name='outros_perfis'),
    path('visualizar_perfil/<int:user_id>/', views.visualizar_perfil, name='visualizar_perfil'),
    path('buscar-matches/', views.buscar_matches, name='buscar_matches'),
    path('adicionar_amizade/<int:user_id>/', views.adicionar_amizade, name='adicionar_amizade'),
    path('teste/', views.teste, name='teste'),
    path('excluir_amizade/<int:amigo_id>/', views.excluir_amizade, name='excluir_amizade'),


] 

