# Generated by Django 3.0.5 on 2020-04-24 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0020_auto_20200420_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='average_rating',
            field=models.IntegerField(default=5),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=500)),
                ('rating', models.IntegerField(default=1)),
                ('reviewer', models.EmailField(max_length=40)),
                ('reviewer_fname', models.CharField(blank=True, max_length=10)),
                ('reviewer_lname', models.CharField(blank=True, max_length=10)),
                ('reviewee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complainant_email', models.EmailField(max_length=40)),
                ('complainant_fname', models.CharField(max_length=10)),
                ('complainant_lname', models.CharField(max_length=10)),
                ('complaint', models.CharField(max_length=500)),
                ('complain_against', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
