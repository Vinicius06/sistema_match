# Generated by Django 4.2.2 on 2023-07-07 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0020_preferencias2_userprofile_livros_preferidos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preferencias2',
            old_name='filme',
            new_name='livro',
        ),
    ]