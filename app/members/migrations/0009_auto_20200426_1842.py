# Generated by Django 3.0.5 on 2020-04-26 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20200414_2137'),
        ('members', '0008_auto_20200419_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedlocation',
            name='locate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_selected_locations', to='location.Locate'),
        ),
        migrations.AlterField(
            model_name='selectedlocation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_selected_locations', to=settings.AUTH_USER_MODEL),
        ),
    ]