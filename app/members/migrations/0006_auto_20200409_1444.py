# Generated by Django 3.0.4 on 2020-04-09 05:44

import core.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20200404_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '유저', 'verbose_name_plural': '유저'},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', core.managers.CustomModelManager()),
            ],
        ),
    ]