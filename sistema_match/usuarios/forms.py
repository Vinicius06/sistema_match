"""
Módulo de formulários para usuários.
"""

from django import forms
from .models import UserProfile, Amizade
from django.contrib.auth import get_user_model
from django.db import models


class UserProfileForm(forms.ModelForm):
    """Formulário para atualização do perfil do usuário."""
    class Meta:
        model = UserProfile
        fields = ['profile_image']

class UploadForm(forms.Form):
    """Formulário para upload de fotos."""
    photo = forms.ImageField()



class SearchForm(forms.Form):
    """Formulário para realizar busca."""
    search_query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Digite sua busca'}))

class PreferenciasFilmesForm(forms.ModelForm):
    """Formulário para selecionar preferências de filmes."""
    class Meta:
        model = UserProfile
        fields = ['filmes_preferidos']
        widgets = {
            'filmes_preferidos': forms.CheckboxSelectMultiple,
        }

class AdicionarFilmeForm(forms.Form):
    """Formulário para adicionar um filme."""
    filme = forms.CharField(max_length=100)

class PreferenciasLivrosForm(forms.ModelForm):
    """Formulário para selecionar preferências de livros."""
    class Meta:
        model = UserProfile
        fields = ['livros_preferidos']
        widgets = {
            'livros_preferidos': forms.CheckboxSelectMultiple,
        }

class AdicionarLivroForm(forms.Form):
    """Formulário para adicionar um livro."""
    livro = forms.CharField(max_length=100)

class PreferenciasSeriesForm(forms.ModelForm):
    """Formulário para selecionar preferências de séries."""
    class Meta:
        model = UserProfile
        fields = ['series_preferidos']
        widgets = {
            'series_preferidos': forms.CheckboxSelectMultiple,
        }

class AdicionarSerieForm(forms.Form):
    """Formulário para adicionar uma série."""
    serie = forms.CharField(max_length=100)

class PreferenciasAnimacoesForm(forms.ModelForm):
    """Formulário para selecionar preferências de animações."""
    class Meta:
        model = UserProfile
        fields = ['animacoes_preferidos']
        widgets = {
            'animacoes_preferidos': forms.CheckboxSelectMultiple,
        }

class AdicionarAnimacaoForm(forms.Form):
    """Formulário para adicionar uma animação."""
    animacao = forms.CharField(max_length=100)

class AdicionarAmigoForm(forms.Form):
    """Formulário para adicionar um amigo."""
    amigo_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user is None:
            raise forms.ValidationError('O usuário não está definido.')

        return cleaned_data

    def save(self):
        if self.user is None:
            return None

        amigo_id = self.cleaned_data.get('amigo_id')
        amigo = get_user_model().objects.filter(id=amigo_id).first()

        if amigo:
            amizade, created = Amizade.objects.get_or_create(
                usuario_origem=self.user,
                usuario_destino=amigo
            )

class OutrosPerfisForm(forms.ModelForm):
    """Formulário para exibir outros perfis de usuários."""
    amigo_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = []

class MensagemForm(forms.Form):
    """Formulário para enviar uma mensagem."""
    conteudo = forms.CharField(widget=forms.Textarea)


class MarcarMensagemLidaForm(forms.Form):
    """Formulário para marcar uma mensagem como lida."""
    mensagem_id = forms.IntegerField(widget=forms.HiddenInput())
