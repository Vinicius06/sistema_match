from django import forms
from .models import UserProfile, Preferencias_filme, Preferencias_livro, Preferencias_animacao, Preferencias_serie, Amizade
from django.contrib.auth import get_user_model
from django.db import models

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']


class UploadForm(forms.Form):
    photo = forms.ImageField()



class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Digite sua busca'}))

class PhraseForm(forms.Form):
    phrase = forms.CharField(max_length=100)

class PreferenciasFilmesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['filmes_preferidos']
        widgets = {
            'filmes_preferidos': forms.CheckboxSelectMultiple,
        }

class AdicionarFilmeForm(forms.Form):
    filme = forms.CharField(max_length=100)

class PreferenciasLivrosForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['livros_preferidos']
        widgets = {
            'livros_preferidos': forms.CheckboxSelectMultiple,
        }

class AdicionarLivroForm(forms.Form):
    livro = forms.CharField(max_length=100)

class PreferenciasSeriesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['series_preferidos']
        widgets = {
            'series_preferidos': forms.CheckboxSelectMultiple,
        }

class AdicionarSerieForm(forms.Form):
    serie = forms.CharField(max_length=100)

class PreferenciasAnimacoesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['animacoes_preferidos']
        widgets = {
            'animacoes_preferidos': forms.CheckboxSelectMultiple,
        }

class AdicionarAnimacaoForm(forms.Form):
    animacao = forms.CharField(max_length=100)

class AdicionarAmigoForm(forms.Form):
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
    amigo_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = []