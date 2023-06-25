import pytest
from django.contrib.auth.models import User
from django.test import Client
from usuarios.models import UserProfile

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


