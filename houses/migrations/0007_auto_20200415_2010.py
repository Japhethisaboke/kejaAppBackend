# Generated by Django 3.0.5 on 2020-04-15 17:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0006_auto_20200415_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to='media/house_images/%y/%m/%d'), null=True, size=None),
        ),
    ]
