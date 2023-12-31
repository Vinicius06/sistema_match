from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import UserProfile, User, Preferencias_filme
from .models import Preferencias_livro, Preferencias_animacao, Preferencias_serie, Amizade, Mensagem, CaixaEntrada
from django.contrib.auth import logout
from .forms import UserProfileForm, SearchForm, AdicionarFilmeForm, AdicionarLivroForm, MensagemForm, MarcarMensagemLidaForm
from .forms import AdicionarAnimacaoForm, AdicionarSerieForm, AdicionarAmigoForm, OutrosPerfisForm
from django.contrib import messages
from django.db.models import Q

# View responsável pelo cadastro de usuários

def teste(request):
    return render(request, 'teste.html' )

#História de Usuário EU001:
#Eu como <usuario> quero conseguir me cadastrar no sistema.
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
            return HttpResponse('Já existe um usuario com esse username(VOLTE A PAGINA NÃO CRIEI UM RETORNO)')

        # Criar e salvar um novo usuário

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        profile = UserProfile(user=user)
        profile.save()
        return HttpResponse('Usuário cadastrado com sucesso!(VOLTE A PAGINA NÃO CRIEI UM RETORNO)')


#História de Usuário EU002:
#Eu como <usuario> quero conseguir logar no sistema.
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
            error_message = 'Email ou senha inválidos.'
            messages.error(request, error_message)
            return redirect('home')



#História de Usuário EU003:
#Eu como <usuario> quero conseguir entrar na plataforma ao logar no sistema.
 # View da plataforma que requer autenticação
@login_required(login_url="/login/")
def plataforma(request):
    user_profile = UserProfile.objects.get(user=request.user)
    amigos = user_profile.amigos.all()
    context = {'user_profile': user_profile,
               'amigos': amigos,}
    return render(request, 'plataforma.html', context)

#História de Usuário EU004:
#Eu como <usuario> quero conseguir deslogar do sistema.
@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login/")
def perfil(request):
    user_profile = UserProfile.objects.get(user=request.user)
    amigos = user_profile.amigos.all()
    context = {'user_profile': user_profile,
               'amigos':amigos, }
    return render(request, 'perfil.html', context)

#História de Usuário EU005:
#Eu como <usuario> quero conseguir visualizar meu perfil.
@login_required(login_url="/login/")
def profile_usuario(request):
    user_profile = UserProfile.objects.get(user=request.user)
    amigos = user_profile.amigos.all()
    filmes_preferidos = user_profile.filmes_preferidos.all()
    livros_preferidos = user_profile.livros_preferidos.all()
    series_preferidos = user_profile.series_preferidos.all()
    animacoes_preferidos = user_profile.animacoes_preferidos.all()

    context = {
        'user_profile': user_profile,
        'filmes_preferidos': filmes_preferidos,
        'livros_preferidos': livros_preferidos,
        'series_preferidos': series_preferidos,
        'animacoes_preferidos': animacoes_preferidos,
        'amigos': amigos,
    }
    return render(request, 'profile_usuario.html', context)


#História de Usuário EU006:
#Eu como <usuario> quero conseguir ir nas configurações do meu perfil.
@login_required(login_url="/login/")
def configuracoes(request):
    user_profile = UserProfile.objects.get(user=request.user)
    amigos = user_profile.amigos.all()
    context = {
        'user_profile': user_profile,
        'amigos': amigos,
    }
    return render(request, 'configuracoes.html', context )

@login_required
def my_view(request):
    options = ['meu_perfil', 'configuracoes', 'logout']
    return render(request, 'plataforma.html', {'options': options})


#História de Usuário EU007:
#Eu como <usuario> quero conseguir visualizar meus filmes favoritos.
@login_required(login_url="/login/")
def filmes(request):
    user_profile = request.user.userprofile
    amigos = user_profile.amigos.all()
    filmes_preferidos = user_profile.filmes_preferidos.all()
    context = {
        'user_profile': user_profile,
        'filmes_preferidos': filmes_preferidos,
        'amigos': amigos,
    }
    return render(request, 'filmes.html', context)

#História de Usuário EU008:
#Eu como <usuario> quero conseguir visualizar meus livros favoritos.
@login_required(login_url="/login/")
def livros(request):
    user_profile = request.user.userprofile
    livros_preferidos = user_profile.livros_preferidos.all()
    amigos = user_profile.amigos.all()
    context = {
        'user_profile': user_profile,
        'livros_preferidos': livros_preferidos,
        'amigos': amigos
    }
    return render(request, 'livros.html', context)


#História de Usuário EU009:
#Eu como <usuario> quero conseguir visualizar minhas series favoritas.
@login_required(login_url="/login/")
def series(request):
    user_profile = request.user.userprofile
    series_preferidos = user_profile.series_preferidos.all()
    amigos = user_profile.amigos.all()
    context = {
        'user_profile': user_profile,
        'series_preferidos': series_preferidos,
        'amigos': amigos
    }
    return render(request, 'series.html', context)


#História de Usuário EU010:
#Eu como <usuario> quero conseguir visualizar minhas animações favoritas.
@login_required(login_url="/login/")
def animacoes(request):
    user_profile = request.user.userprofile
    animacoes_preferidos = user_profile.animacoes_preferidos.all()
    amigos = user_profile.amigos.all()
    context = {
        'user_profile': user_profile,
        'animacoes_preferidos': animacoes_preferidos,
        'amigos': amigos,
    }
    return render(request, 'animacoes.html', context)


@login_required(login_url="/login/")
def search(request):
    form = SearchForm(request.GET)
    user_profile = request.user.userprofile
    amigos = user_profile.amigos.all()
    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        # Salve o valor da busca em uma lista ou banco de dados, por exemplo:
        # SearchHistory.objects.create(search_query=search_query)
        # Ou adicione o valor à uma lista em sessão:
        # request.session.setdefault('search_history', []).append(search_query)

        # Realize a lógica de busca com base no search_query
        results = perform_search(search_query)

        context = {
            'form': form,
            'results': results,
        }
        return render(request, 'filmes.html', context)

    context = {
        'user_profile': user_profile,
        'form': form,
        'amigos': amigos,
    }
    return render(request, 'filmes.html', context)


#História de Usuário EU011:
#Eu como <usuario> quero conseguir mudar minha foto de perfil.
@login_required(login_url="/login/")
def upload_image(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('upload_image')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'perfil.html', {'form': form, 'user_profile': user_profile})

#História de Usuário EU012:
#Eu como <usuario> quero conseguir adicionar meu filme favorito.
@login_required(login_url="/login/")
def filme_usuario(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = AdicionarFilmeForm(request.POST)
        if form.is_valid():
            filme = form.cleaned_data['filme']


            # Crie um novo objeto de filme preferido
            filme_preferido = Preferencias_filme(filme=filme)
            filme_preferido.save()

            # Adicione o filme preferido ao perfil do usuário
            user_profile.filmes_preferidos.add(filme_preferido)
            user_profile.save()

            # Redirecionar para a página de filmes após adicionar o filme preferido
            return redirect('filmes')
    else:
        form = AdicionarFilmeForm()

    return render(request, 'perfil.html', {'form': form, 'user_profile': user_profile})


#História de Usuário EU012:
#Eu como <usuario> quero conseguir deletar o filme da minhas preferencias.
@login_required(login_url="/login/")
def deletar_filme(request, filme_id):
    user_profile = request.user.userprofile

    # Verificar se o filme existe no perfil do usuário
    try:
        filme_preferido = user_profile.filmes_preferidos.get(id=filme_id)
    except Preferencias_filme.DoesNotExist:
        return HttpResponse('Filme não encontrado.')

    # Remover o filme do perfil do usuário
    user_profile.filmes_preferidos.remove(filme_preferido)
    user_profile.save()

    return redirect('filmes')  # Redirecionar para a página de filmes após deletar o filme

#História de Usuário EU013:
#Eu como <usuario> quero conseguir adicionar meu livro favorito.
@login_required(login_url="/login/")
def livro_usuario(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = AdicionarLivroForm(request.POST)
        if form.is_valid():
            livro = form.cleaned_data['livro']


            # Crie um novo objeto de filme preferido
            livro_preferido = Preferencias_livro(livro=livro)
            livro_preferido.save()

            # Adicione o filme preferido ao perfil do usuário
            user_profile.livros_preferidos.add(livro_preferido)
            user_profile.save()

            # Redirecionar para a página de filmes após adicionar o filme preferido
            return redirect('livros')
    else:
        form = AdicionarLivroForm()

    return render(request, 'perfil.html', {'form': form, 'user_profile': user_profile})


#História de Usuário EU014:
#Eu como <usuario> quero conseguir deletar o livro da minhas preferencias.
@login_required(login_url="/login/")
def deletar_livro(request, livro_id):
    user_profile = request.user.userprofile

    # Verificar se o filme existe no perfil do usuário
    try:
        livro_preferido = user_profile.livros_preferidos.get(id=livro_id)
    except Preferencias_livro.DoesNotExist:
        return HttpResponse('livro não encontrado.')

    # Remover o filme do perfil do usuário
    user_profile.livros_preferidos.remove(livro_preferido)
    user_profile.save()

    return redirect('livros')  # Redirecionar para a página de filmes após deletar o filme


#História de Usuário EU015:
#Eu como <usuario> quero conseguir adicionar minhas series favoritas.
@login_required(login_url="/login/")
def serie_usuario(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = AdicionarSerieForm(request.POST)
        if form.is_valid():
            serie = form.cleaned_data['serie']


            # Crie um novo objeto de filme preferido
            serie_preferido = Preferencias_serie(serie=serie)
            serie_preferido.save()

            # Adicione o filme preferido ao perfil do usuário
            user_profile.series_preferidos.add(serie_preferido)
            user_profile.save()

            # Redirecionar para a página de filmes após adicionar o filme preferido
            return redirect('series')
    else:
        form = AdicionarSerieForm()

    return render(request, 'perfil.html', {'form': form, 'user_profile': user_profile})


#História de Usuário EU016:
#Eu como <usuario> quero conseguir deletar a serie da minhas preferencias.
@login_required(login_url="/login/")
def deletar_serie(request, serie_id):
    user_profile = request.user.userprofile

    # Verificar se o filme existe no perfil do usuário
    try:
        serie_preferido = user_profile.series_preferidos.get(id=serie_id)
    except Preferencias_serie.DoesNotExist:
        return HttpResponse('Serie não encontrada.')

    # Remover o filme do perfil do usuário
    user_profile.series_preferidos.remove(serie_preferido)
    user_profile.save()

    return redirect('series')  # Redirecionar para a página de filmes após deletar o filme


#História de Usuário EU017:
#Eu como <usuario> quero conseguir adicionar minhas animações favoritas.
@login_required(login_url="/login/")
def animacao_usuario(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = AdicionarAnimacaoForm(request.POST)
        if form.is_valid():
            animacao = form.cleaned_data['animacao']


            # Crie um novo objeto de filme preferido
            animacao_preferido = Preferencias_animacao(animacao=animacao)
            animacao_preferido.save()

            # Adicione o filme preferido ao perfil do usuário
            user_profile.animacoes_preferidos.add(animacao_preferido)
            user_profile.save()

            # Redirecionar para a página de filmes após adicionar o filme preferido
            return redirect('animacoes')
    else:
        form = AdicionarAnimacaoForm()

    return render(request, 'perfil.html', {'form': form, 'user_profile': user_profile})


#História de Usuário EU018:
#Eu como <usuario> quero conseguir deletar a animação da minhas preferencias.
@login_required(login_url="/login/")
def deletar_animacao(request, animacao_id):
    user_profile = request.user.userprofile

    # Verificar se o filme existe no perfil do usuário
    try:
        animacao_preferido = user_profile.animacoes_preferidos.get(id=animacao_id)
    except Preferencias_animacao.DoesNotExist:
        return HttpResponse('animacao não encontrado.')

    # Remover o filme do perfil do usuário
    user_profile.animacoes_preferidos.remove(animacao_preferido)
    user_profile.save()

    return redirect('animacoes')  # Redirecionar para a página de filmes após deletar o filme

#História de Usuário EU019:
#Eu como <usuario> quero conseguir visualizar outro perfis.
@login_required(login_url="/login/")
def outros_perfis(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    user_preferences = get_object_or_404(user=user)
    adicionar_amigo_form = AdicionarAmigoForm(user=request.user) 
    amigos = user_profile.amigos.all()

    if request.method == 'POST':
        form = OutrosPerfisForm(request.POST)
        adicionar_amigo_form = AdicionarAmigoForm(request.POST, user=request.user)

        if adicionar_amigo_form.is_valid():
            adicionar_amigo_form.save()
            return redirect('plataforma')
    else:
        form = OutrosPerfisForm(initial={'amigo_id': user.id})

    context = {
        'user_profile': user_profile,
        'user_preferences': user_preferences,
        'adicionar_amigo_form': adicionar_amigo_form,
        'form': form,
        'amigos': amigos,
    }
    return render(request, 'outros_perfis.html', context)


#História de Usuário EU020:
#Eu como <usuario> quero conseguir procurar outros perfis.
@login_required(login_url="/login/")
def search_profiles(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        users = User.objects.filter(username__icontains=query)
        profiles = UserProfile.objects.filter(user__in=users)
        return render(request, 'search_profiles.html', {'profiles': profiles, 'query': query})
    return redirect('home')


#História de Usuário EU021:
#Eu como <usuario> quero conseguir visualizar algum perfil em especifico.
@login_required(login_url="/login/")
def visualizar_perfil(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    return render(request, 'outros_perfis.html', {'user_profile': user_profile})

#História de Usuário EU022:
#Eu como <usuario> quero conseguir buscar matchs.
@login_required(login_url="/login/")
def buscar_matches(request):
    user_profile = UserProfile.objects.get(user=request.user)
    preferencias_filme = user_profile.filmes_preferidos.values('filme')
    preferencias_livro = user_profile.livros_preferidos.values('livro')
    preferencias_serie = user_profile.series_preferidos.values('serie')
    preferencias_animacao = user_profile.animacoes_preferidos.values('animacao')

    matching_users = UserProfile.objects.exclude(user=request.user).filter(
        Q(filmes_preferidos__filme__in=preferencias_filme) |
        Q(livros_preferidos__livro__in=preferencias_livro) |
        Q(series_preferidos__serie__in=preferencias_serie) |
        Q(animacoes_preferidos__animacao__in=preferencias_animacao)
    ).distinct()

    context = {
        'matching_users': matching_users,
    }

    return render(request, 'matches.html', context)


#História de Usuário EU023:
#Eu como <usuario> quero conseguir adicionar um match em especifico.
@login_required(login_url='/login/')
def adicionar_amizade(request, user_id):
    usuario_destino = get_object_or_404(User, id=user_id)

    # Verifica se o usuário de destino não é o próprio usuário logado
    if usuario_destino == request.user:
        return redirect('profile_usuario')

    # Verifica se a amizade já existe
    if request.user.userprofile.amigos.filter(id=usuario_destino.id).exists():
        return redirect('profile_usuario')

    # Cria uma nova amizade
    amizade = Amizade(usuario_origem=request.user, usuario_destino=usuario_destino)
    amizade.save()

    # Adiciona o amigo ao perfil do usuário logado
    request.user.userprofile.amigos.add(usuario_destino)

    return redirect('profile_usuario')


#História de Usuário EU024:
#Eu como <usuario> quero conseguir deletar um match em especifico.
@login_required(login_url='/login/')
def excluir_amizade(request, amigo_id):
    amigo = get_object_or_404(User, id=amigo_id)

    # Verifica se a amizade existe
    if request.user.userprofile.amigos.filter(id=amigo.id).exists():
        # Remove a amizade do perfil do usuário logado
        request.user.userprofile.amigos.remove(amigo)

        # Exclui a amizade do banco de dados
        Amizade.objects.filter(usuario_origem=request.user, usuario_destino=amigo).delete()

    return redirect('profile_usuario')


#História de Usuário EU025:
#Eu como <usuario> quero conseguir visualizar as pessoas que eu dei match.
@login_required(login_url="/login/")
def meus_matchs(request):
    user_profile = UserProfile.objects.get(user=request.user)
    amigos = user_profile.amigos.all()
    context = {'user_profile': user_profile,
               'amigos': amigos,}
    return render(request, 'meus_matchs.html', context)


#História de Usuário EU026:
#Eu como <usuario> quero conseguir enviar mensagens pros meus matchs.
@login_required(login_url="/login/")
def enviar_mensagem(request, username):
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            remetente = request.user
            destinatario = User.objects.get(username=username)
            conteudo = form.cleaned_data['conteudo']
            mensagem = Mensagem.objects.create(remetente=remetente, destinatario=destinatario, conteudo=conteudo)
            return redirect('enviar_mensagem', username=username)
    else:
        form = MensagemForm()
    mensagens = Mensagem.objects.filter(remetente=request.user, destinatario__username=username) | Mensagem.objects.filter(remetente__username=username, destinatario=request.user).order_by('data_envio')
    return render(request, 'enviar_mensagem.html', {'form': form, 'mensagens': mensagens, 'username': username})

#História de Usuário EU027:
#Eu como <usuario> quero conseguir visualizar as mensagens que eu recebo dos meus matchs.
@login_required(login_url="/login/")
def caixa_entrada(request):
    try:
        caixa_entrada = CaixaEntrada.objects.get(usuario=request.user)
    except CaixaEntrada.DoesNotExist:
        caixa_entrada = CaixaEntrada.objects.create(usuario=request.user)

    mensagens = caixa_entrada.mensagens.all()
    
    if request.method == 'POST':
        form = MarcarMensagemLidaForm(request.POST)
        if form.is_valid():
            mensagem_id = form.cleaned_data['mensagem_id']
            mensagem = get_object_or_404(Mensagem, pk=mensagem_id)
            
            if mensagem.destinatario == request.user:
                # Marcar a mensagem como lida
                # Implemente a lógica adequada para atualizar o estado da mensagem como lida
                
                return redirect('caixa_entrada')
    else:
        form = MarcarMensagemLidaForm()
    
    context = {
        'mensagens': mensagens,
        'form': form,
    }
    
    return render(request, 'caixa_entrada.html', context)


@login_required(login_url="/login/")
def marcar_lida(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    mensagem.lida = True
    mensagem.save()

    # Remover a mensagem da lista de mensagens na caixa de entrada
    caixa_entrada = CaixaEntrada.objects.get(usuario=request.user)
    mensagens = caixa_entrada.mensagens.exclude(id=mensagem_id)

    # Atualizar o contexto e renderizar o template novamente
    context = {
        'mensagens': mensagens
    }

    return render(request, 'caixa_entrada.html', context)