# Generated by Django 4.2.2 on 2023-07-07 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0018_rename_filme_preferencias_titulo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preferencias',
            old_name='titulo',
            new_name='filme',
        ),
    ]
