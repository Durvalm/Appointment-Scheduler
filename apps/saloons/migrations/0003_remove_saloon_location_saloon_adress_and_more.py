# Generated by Django 4.0.6 on 2022-07-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saloons', '0002_remove_saloon_barbers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saloon',
            name='location',
        ),
        migrations.AddField(
            model_name='saloon',
            name='adress',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='saloon',
            name='street_number',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
