# Generated by Django 4.2.2 on 2023-07-07 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0012_userprofile_is_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_default',
        ),
    ]
