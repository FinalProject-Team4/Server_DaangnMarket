# Generated by Django 3.0.4 on 2020-04-07 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_postlike_recommendword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_images', to='post.Post'),
        ),
    ]