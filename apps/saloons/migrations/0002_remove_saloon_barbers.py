# Generated by Django 4.0.6 on 2022-07-11 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saloons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saloon',
            name='barbers',
        ),
    ]
