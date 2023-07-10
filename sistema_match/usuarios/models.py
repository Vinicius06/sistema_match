from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Preferencias_filme(models.Model):
    filme = models.CharField(max_length=100)

class Preferencias_livro(models.Model):
    livro = models.CharField(max_length=100)

class Preferencias_serie(models.Model):
    serie = models.CharField(max_length=100)    

class Preferencias_animacao(models.Model):
    animacao = models.CharField(max_length=100)    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amigos = models.ManyToManyField(User, related_name='amigos+')
    profile_image = models.ImageField(upload_to='profile_images/')
    filmes_preferidos = models.ManyToManyField(Preferencias_filme)
    livros_preferidos = models.ManyToManyField(Preferencias_livro)
    series_preferidos = models.ManyToManyField(Preferencias_serie)
    animacoes_preferidos = models.ManyToManyField(Preferencias_animacao)
    

    def __str__(self):
        return self.user.username
    
class Amizade(models.Model):
    usuario_origem = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amigos_origem')
    usuario_destino = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amigos_destino')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario_origem.username} -> {self.usuario_destino.username}'
    
class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.remetente.username} -> {self.destinatario.username}'
    
class CaixaEntrada(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    mensagens = models.ManyToManyField(Mensagem, blank=True, related_name='caixa_entrada')
    
    def __str__(self):
        return self.usuario.username