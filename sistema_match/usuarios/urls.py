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
    path('plataforma/filmes/', views.filmes, name='filmes'),
    path('plataforma/series/', views.series, name='series'),
    path('plataforma/animacoes/', views.animacoes, name='animacoes'),
    path('plataforma/livros/', views.livros, name='livros'),
    path('search_profiles/', views.search_profiles, name='search_profiles'), 
    path('upload-image/', views.upload_image, name='upload_image'),
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),
    path('deletar_filme/<int:filme_id>/', views.deletar_filme, name='deletar_filme'),
    path('perfil_usuario2/', views.perfil_usuario2, name='perfil_usuario2'),
    path('deletar_livro/<int:livro_id>/', views.deletar_livro, name='deletar_livro'),




] 

