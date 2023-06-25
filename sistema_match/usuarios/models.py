from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos', blank=True)

    # Adicione outros campos desejados para o perfil do usuário

    def __str__(self):
        return self.user.username
