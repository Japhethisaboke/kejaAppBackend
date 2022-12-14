# Generated by Django 3.0.5 on 2020-04-16 11:38

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0009_auto_20200415_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='images',
        ),
        migrations.AddField(
            model_name='house',
            name='master_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='media/master_image/%y/%m/%d'),
        ),
        migrations.CreateModel(
            name='HouseImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='media/house_images/%y/%m/%d')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.House')),
            ],
        ),
    ]
