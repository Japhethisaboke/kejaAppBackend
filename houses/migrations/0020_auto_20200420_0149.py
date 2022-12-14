# Generated by Django 3.0.5 on 2020-04-19 22:49

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0019_auto_20200417_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='media/profile_picture/%y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='house',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
    ]
