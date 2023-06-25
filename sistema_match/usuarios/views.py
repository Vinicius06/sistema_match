from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# View responsável pelo cadastro de usuários

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else: 
         # Obter os dados enviados pelo formulário de cadastro
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verificar se já existe um usuário com o mesmo username
        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuario com esse username')
        
        # Criar e salvar um novo usuário

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        profile = UserProfile(user=user)
        profile.save()
        return HttpResponse('Usuário cadastrado com sucesso!')


# View responsável pelo login dos usuários
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        # Obter os dados enviados pelo formulário de login
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        # Autenticar o usuário
        user = authenticate(username=username, password=senha)
        
        if user: 
            # Realizar o login do usuário e redirecionar para a página da plataforma
            login_django(request, user)
            return redirect('/plataforma/')
            
        else: 
            return HttpResponse('Email ou senha invalidos')

 # View da plataforma que requer autenticação       
@login_required(login_url="/login/")
def plataforma(request):
        return render(request, 'plataforma.html')