import pytest
from django.contrib.auth.models import User
from django.test import Client
from usuarios.models import UserProfile, Preferencias_filme, Preferencias_animacao, Preferencias_livro, Preferencias_serie
from usuarios.forms import AdicionarAmigoForm, OutrosPerfisForm
from django.shortcuts import reverse, get_object_or_404, redirect
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.contrib.auth.decorators import login_required

@pytest.mark.django_db
def test_cadastro_usuario():
    client = Client()

    # Simula uma requisição POST para a rota de cadastro
    response = client.post('/cadastro/', {
        'username': 'novousuario',
        'email': 'novousuario@example.com',
        'senha': 'novasenha',
    })

    # Verifica se a resposta HTTP é 200 (OK)
    assert response.status_code == 200

    # Verifica se o usuário foi criado com sucesso
    user = User.objects.get(username='novousuario')
    assert user is not None

    # Verifica se o perfil de usuário foi criado com sucesso
    profile = UserProfile.objects.get(user=user)
    assert profile is not None


@pytest.mark.django_db
def test_cadastro_usuario_existente():
    client = Client()

    # Criar um usuário existente no banco de dados
    User.objects.create_user(username='usuarioexistente', email='usuarioexistente@example.com', password='senhaexistente')

    # Simular uma requisição POST para a rota de cadastro
    response = client.post('/cadastro/', {
        'username': 'usuarioexistente',
        'email': 'novousuario@example.com',
        'senha': 'novasenha',
    })

    # Verificar se a resposta possui o status HTTP 200 (OK)
    assert response.status_code == 200

    # Decodificar a resposta para uma string
    response_text = response.content.decode('utf-8')

    # Verificar se a resposta contém a mensagem de erro adequada
    assert 'Já existe um usuario com esse username' in response_text

@pytest.mark.django_db
def test_login_usuario_sucesso():
    client = Client()

    # Criar um usuário no banco de dados
    User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Simular uma requisição POST para a rota de login
    response = client.post('/login/', {
        'username': 'usuarioteste',
        'senha': 'senhateste',
    })

    # Verificar se a resposta possui o status de redirecionamento (302)
    assert response.status_code == 302

    # Verificar se o redirecionamento leva à página correta
    assert response.url == '/plataforma/'


@pytest.mark.django_db
def test_logout_usuario():
    client = Client()

    # Criar um usuário no banco de dados
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Realizar o login do usuário
    client.login(username='usuarioteste', password='senhateste')

    # Verificar se o usuário está autenticado antes do logout
    assert client.session['_auth_user_id'] == str(user.id)

    # Simular uma requisição GET para a rota de logout
    response = client.get('/logout/')

    # Verificar se a resposta possui um status de redirecionamento (302)
    assert response.status_code == 302

    # Verificar se o redirecionamento leva à página correta
    assert response.url == '/'

    # Verificar se o usuário foi deslogado corretamente
    assert '_auth_user_id' not in client.session

@pytest.mark.django_db
def test_adicionar_amizade():
    client = Client()

    # Criar dois usuários no banco de dados
    usuario1 = User.objects.create_user(username='usuario1', email='usuario1@example.com', password='senha1')
    usuario2 = User.objects.create_user(username='usuario2', email='usuario2@example.com', password='senha2')

    # Criar perfil de usuário para o primeiro usuário
    UserProfile.objects.create(user=usuario1)

    # Realizar o login do primeiro usuário
    client.login(username='usuario1', password='senha1')

    # Simular uma requisição POST para a rota de adicionar amizade
    response = client.post(f'/adicionar_amizade/{usuario2.id}/')

    # Verificar se a resposta possui um status de redirecionamento (302)
    assert response.status_code == 302

    # Verificar se o redirecionamento leva à página correta (sem verificar a URL completa)
    assert response.url == '/profile_usuario/'

@pytest.mark.django_db
def test_excluir_amizade():
    client = Client()

    # Criar dois usuários no banco de dados
    usuario1 = User.objects.create_user(username='usuario1', email='usuario1@example.com', password='senha1')
    usuario2 = User.objects.create_user(username='usuario2', email='usuario2@example.com', password='senha2')

    # Criar perfil de usuário para o primeiro usuário
    UserProfile.objects.create(user=usuario1)

    # Realizar o login do primeiro usuário
    client.login(username='usuario1', password='senha1')

    # Adicionar uma amizade entre os dois usuários
    usuario1.userprofile.amigos.add(usuario2)

    # Verificar se a amizade existe antes de excluir
    assert usuario1.userprofile.amigos.filter(id=usuario2.id).exists()

    # Simular uma requisição POST para a rota de excluir amizade
    response = client.post(f'/excluir_amizade/{usuario2.id}/')

    # Verificar se a resposta possui um status de redirecionamento (302)
    assert response.status_code == 302

    # Verificar se a amizade foi removida corretamente
    assert not usuario1.userprofile.amigos.filter(id=usuario2.id).exists()


@pytest.mark.django_db
def test_perfil_usuario():
    client = Client()

    # Criar um usuário no banco de dados
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Criar perfil de usuário para o usuário
    UserProfile.objects.create(user=user)

    # Realizar o login do usuário
    client.login(username='usuarioteste', password='senhateste')

    # Simular uma requisição GET para a rota de perfil
    response = client.get('/perfil/')

    # Verificar se a resposta possui um status de sucesso (200)
    assert response.status_code == 200

    # Verificar se o usuário correto está sendo exibido no perfil
    assert response.context['user'] == user


@pytest.mark.django_db
def test_criar_usuario():
    # Criar um usuário
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Verificar se o usuário foi criado corretamente
    assert User.objects.count() == 1
    assert user.username == 'usuarioteste'
    assert user.email == 'usuarioteste@example.com'

@pytest.mark.django_db
def test_adicionar_filme_preferido(client):
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')
    user_profile = UserProfile.objects.create(user=user)
    client.login(username='usuarioteste', password='senhateste')
    response = client.post(reverse('filme_usuario'), {
        'filme': 'Filme de teste',
    })
    assert response.status_code == 302
    assert Preferencias_filme.objects.filter(filme='Filme de teste', userprofile=user_profile).exists()

@pytest.mark.django_db
def test_deletar_filme_preferido(client):
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')
    user_profile = UserProfile.objects.create(user=user)
    filme_preferido = Preferencias_filme.objects.create(filme='Filme de teste', userprofile=user_profile)
    user_profile.filmes_preferidos.add(filme_preferido)
    client.login(username='usuarioteste', password='senhateste')
    response = client.post(reverse('deletar_filme', args=[filme_preferido.id]))
    assert response.status_code == 302
    assert not Preferencias_filme.objects.filter(id=filme_preferido.id, userprofile=user_profile).exists()


@pytest.mark.django_db
def test_adicionar_serie_preferido(client):
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')
    user_profile = UserProfile.objects.create(user=user)
    client.login(username='usuarioteste', password='senhateste')
    response = client.post(reverse('serie_usuario'), {
        'serie': 'Serie de teste',
    })
    assert response.status_code == 302
    assert Preferencias_serie.objects.filter(serie='Serie de teste', userprofile=user_profile).exists()

@pytest.mark.django_db
def test_deletar_serie_preferido(client):
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')
    user_profile = UserProfile.objects.create(user=user)
    serie_preferido = Preferencias_serie.objects.create(serie='Serie de teste', userprofile=user_profile)
    user_profile.series_preferidos.add(serie_preferido)
    client.login(username='usuarioteste', password='senhateste')
    response = client.post(reverse('deletar_serie', args=[serie_preferido.id]))
    assert response.status_code == 302
    assert not Preferencias_serie.objects.filter(id=serie_preferido.id, userprofile=user_profile).exists()

@pytest.mark.django_db
def test_adicionar_livro_preferido(client):
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')
    user_profile = UserProfile.objects.create(user=user)
    client.login(username='usuarioteste', password='senhateste')
    response = client.post(reverse('livro_usuario'), {
        'livro': 'Livro de teste',
    })
    assert response.status_code == 302
    assert Preferencias_livro.objects.filter(livro='Livro de teste', userprofile=user_profile).exists()

@pytest.mark.django_db
def test_deletar_livro_preferido(client):
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')
    user_profile = UserProfile.objects.create(user=user)
    livro_preferido = Preferencias_livro.objects.create(livro='Livro de teste', userprofile=user_profile)
    user_profile.livros_preferidos.add(livro_preferido)
    client.login(username='usuarioteste', password='senhateste')
    response = client.post(reverse('deletar_livro', args=[livro_preferido.id]))
    assert response.status_code == 302
    assert not Preferencias_livro.objects.filter(id=livro_preferido.id, userprofile=user_profile).exists()

@pytest.mark.django_db
def test_adicionar_animacao_preferido(client):
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')
    user_profile = UserProfile.objects.create(user=user)
    client.login(username='usuarioteste', password='senhateste')
    response = client.post(reverse('animacao_usuario'), {
        'animacao': 'Animacao de teste',
    })
    assert response.status_code == 302
    assert Preferencias_animacao.objects.filter(animacao='Animacao de teste', userprofile=user_profile).exists()

@pytest.mark.django_db
def test_deletar_animacao_preferido(client):
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')
    user_profile = UserProfile.objects.create(user=user)
    animacao_preferido = Preferencias_animacao.objects.create(animacao='Animacao de teste', userprofile=user_profile)
    user_profile.animacoes_preferidos.add(animacao_preferido)
    client.login(username='usuarioteste', password='senhateste')
    response = client.post(reverse('deletar_animacao', args=[animacao_preferido.id]))
    assert response.status_code == 302
    assert not Preferencias_animacao.objects.filter(id=animacao_preferido.id, userprofile=user_profile).exists()

@pytest.mark.django_db
def test_acesso_pagina_inexistente():
    client = Client()

    # Simular uma requisição GET para uma página inexistente
    response = client.get('/pagina_inexistente/')

    # Verificar se a resposta possui o status HTTP 404 (Página não encontrada)
    assert response.status_code == 404

@pytest.mark.django_db
def test_pesquisar_usuario():
    client = Client()

    # Criar um usuário no banco de dados
    User.objects.create_user(username='usuario1', email='usuario1@example.com', password='senha1')

    # Criar um usuário de teste para autenticação
    User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Autenticar o cliente com o usuário de teste
    client.login(username='usuarioteste', password='senhateste')

    # Definir a consulta de pesquisa
    query = 'usuario1'

    # Verificar se a consulta não é None
    assert query is not None

    # Simular uma requisição GET para a rota de pesquisa de usuários
    response = client.get('/search_profiles/', {'query': query})  # Alterado de 'q' para 'query'

    # Verificar se a resposta da requisição é bem-sucedida (status code 200)
    assert response.status_code == 200

    # Verificar se os perfis estão sendo passados para o template
    assert 'profiles' in response.context

    # Verificar se a consulta está sendo passada para o template
    assert 'query' in response.context
    assert response.context['query'] == query

@pytest.mark.django_db
def test_visualizar_perfil():
    client = Client()

    # Criar um usuário de teste para autenticação
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Criar um perfil de usuário para visualização
    user_profile = UserProfile.objects.create(user=user)

    # Autenticar o cliente com o usuário de teste
    client.login(username='usuarioteste', password='senhateste')

    # Simular uma requisição GET para visualizar o perfil
    response = client.get(reverse('visualizar_perfil', args=[user.id]))

    # Verificar se a resposta possui o código de status correto
    assert response.status_code == 200

    # Verificar se o perfil do usuário está presente na resposta
    assert 'user_profile' in response.context
    assert response.context['user_profile'] == user_profile


@pytest.mark.django_db
def test_plataforma():
    client = Client()

    # Criar um usuário de teste para autenticação
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Criar o perfil do usuário
    user_profile = UserProfile.objects.create(user=user)

    # Autenticar o cliente com o usuário de teste
    client.login(username='usuarioteste', password='senhateste')

    # Simular uma requisição GET para acessar a plataforma
    response = client.get(reverse('plataforma'))

    # Verificar se a resposta possui o código de status correto
    assert response.status_code == 200

    # Verificar se o perfil do usuário está presente no contexto da resposta
    assert 'user_profile' in response.context
    assert response.context['user_profile'] == user_profile

    # Verificar se a lista de amigos está presente no contexto da resposta
    assert 'amigos' in response.context
    assert response.context['amigos'].count() == 0  # Verificar se a lista de amigos está vazia inicialmente

@pytest.mark.django_db
def test_configuracoes():
    client = Client()

    # Criar um usuário de teste para autenticação
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Criar o perfil do usuário
    user_profile = UserProfile.objects.create(user=user)

    # Autenticar o cliente com o usuário de teste
    client.login(username='usuarioteste', password='senhateste')

    # Simular uma requisição GET para acessar as configurações
    response = client.get(reverse('configuracoes'))

    # Verificar se a resposta possui o código de status correto
    assert response.status_code == 200

    # Verificar se o perfil do usuário está presente no contexto da resposta
    assert 'user_profile' in response.context
    assert response.context['user_profile'] == user_profile

    # Verificar se a lista de amigos está presente no contexto da resposta
    assert 'amigos' in response.context
    assert response.context['amigos'].count() == 0  # Verificar se a lista de amigos está vazia inicialmente


@pytest.mark.django_db
def test_profile_usuario():
    client = Client()

    # Criar um usuário de teste para autenticação
    user = User.objects.create_user(username='usuarioteste', email='usuarioteste@example.com', password='senhateste')

    # Criar o perfil do usuário
    user_profile = UserProfile.objects.create(user=user)

    # Autenticar o cliente com o usuário de teste
    client.login(username='usuarioteste', password='senhateste')

    # Simular uma requisição GET para acessar o perfil do usuário
    response = client.get(reverse('profile_usuario'))

    # Verificar se a resposta possui o código de status correto
    assert response.status_code == 200

    # Verificar se o perfil do usuário está presente no contexto da resposta
    assert 'user_profile' in response.context
    assert response.context['user_profile'] == user_profile

    # Verificar se as listas de filmes, livros, séries e animações estão presentes no contexto da resposta
    assert 'filmes_preferidos' in response.context
    assert 'livros_preferidos' in response.context
    assert 'series_preferidos' in response.context
    assert 'animacoes_preferidos' in response.context

    # Verificar se a lista de amigos está presente no contexto da resposta
    assert 'amigos' in response.context
    assert response.context['amigos'].count() == 0  # Verificar se a lista de amigos está vazia inicialmente

