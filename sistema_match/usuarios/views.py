from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.views.generic import CreateView
from django.contrib.auth import logout
from .forms import UserProfileForm, UploadForm

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
        
def search_profiles(request):
    if request.method == 'GET':
        query = request.GET.get('query')  # Obter o termo de pesquisa da query string
        if query:
            # Realizar a busca dos perfis de usuário com base no termo de pesquisa
            profiles = User.objects.filter(username__icontains=query).all()
        else:
            profiles = User.objects.none()  # Retorna uma queryset vazia se não houver termo de pesquisa

        context = {
            'profiles': profiles,
            'query': query,
        }
        return render(request, 'search_profiles.html', context)
    else:
        # Método POST não é necessário para a busca de perfis
        return render(request, 'search_profiles.html')
            

 # View da plataforma que requer autenticação       
@login_required(login_url="/login/")
def plataforma(request):
    return render(request, 'plataforma.html')

@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url="/login/")
def perfil(request):
    return render(request, 'perfil.html' )

@login_required(login_url="/login/")
def configuracoes(request):
    return render(request, 'configuracoes.html' )

@login_required
def my_view(request):
    options = ['meu_perfil', 'configuracoes', 'logout']
    return render(request, 'plataforma.html', {'options': options})

@login_required(login_url="/login/")
def filmes(request):
    return render(request, 'filmes.html' )

@login_required(login_url="/login/")
def livros(request):
    return render(request, 'livros.html' )

@login_required(login_url="/login/")
def series(request):
    return render(request, 'series.html' )

@login_required(login_url="/login/")
def animacoes(request):
    return render(request, 'animacoes.html' )

@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UserProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'edit_profile.html', context)

@login_required
def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data['photo']
            # Salve a foto ou faça o processamento desejado
            # por exemplo, user.profile_photo = photo
            # user.save()
            return render(request, 'upload_success.html')
    else:
        form = UploadForm()
    
    return render(request, 'plataforma.html', {'form': form})

@login_required
def change_profile_photo(request):
    profile_photo_url = '/media/path/to/profile_photo.jpg'  # Substitua pelo caminho correto da imagem carregada

    return render(request, 'change_profile_photo.html', {'profile_photo_url': profile_photo_url})