from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_image', )  # Adicione outros campos do perfil, se necessário

class UploadForm(forms.Form):
    photo = forms.ImageField()

