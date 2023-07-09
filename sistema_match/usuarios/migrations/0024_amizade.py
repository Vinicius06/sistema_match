# Generated by Django 4.2.2 on 2023-07-09 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0023_preferencias_animacao_preferencias_serie_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amizade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('usuario_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amigos_destino', to=settings.AUTH_USER_MODEL)),
                ('usuario_origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amigos_origem', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
