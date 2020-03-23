# Generated by Django 3.0.4 on 2020-03-20 07:43

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dong', models.CharField(max_length=20)),
                ('gu', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('latlng', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
            options={
                'verbose_name': '위치 정보 ',
                'verbose_name_plural': '위치 정보  목록',
            },
        ),
    ]