# Generated by Django 4.2.2 on 2023-07-10 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0025_userprofile_amigos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensagens_recebidas', to=settings.AUTH_USER_MODEL)),
                ('remetente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensagens_enviadas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
