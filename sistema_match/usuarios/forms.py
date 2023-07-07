from django import forms
from .models import UserProfile, Preferencias
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

class AdicionarLivrosForm(forms.Form):
    livro = forms.CharField(max_length=100)
