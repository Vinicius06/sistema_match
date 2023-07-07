# Generated by Django 4.2.2 on 2023-07-07 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0019_rename_titulo_preferencias_filme'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferencias2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filme', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='livros_preferidos',
            field=models.ManyToManyField(to='usuarios.preferencias2'),
        ),
    ]