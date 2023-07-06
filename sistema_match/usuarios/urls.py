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
    path('plataforma/series/', views.filmes, name='series'),
    path('plataforma/animacoes/', views.filmes, name='animacoes'),
    path('plataforma/livros/', views.filmes, name='livros'),
    path('search_profiles/', views.search_profiles, name='search_profiles'),



]
