# Generated by Django 3.0.4 on 2020-04-21 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20200421_0121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='showed_locate',
            new_name='showed_locates',
        ),
    ]
