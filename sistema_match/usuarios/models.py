from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Preferencias(models.Model):
    filme = models.CharField(max_length=100)
   


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/')
    filmes_preferidos = models.ManyToManyField(Preferencias)
    

    def __str__(self):
        return self.user.username
    
    
