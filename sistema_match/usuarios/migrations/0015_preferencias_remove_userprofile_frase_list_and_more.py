# Generated by Django 4.2.2 on 2023-07-07 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0014_userprofile_frase_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filme', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='frase_list',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phrases',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='filmes_preferidos',
            field=models.ManyToManyField(to='usuarios.preferencias'),
        ),
    ]