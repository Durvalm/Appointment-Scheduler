# Generated by Django 4.0.6 on 2022-07-21 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbers', '0009_remove_service_price_price_barber_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barber',
            name='price',
        ),
        migrations.AddField(
            model_name='barber',
            name='price',
            field=models.ManyToManyField(blank=True, to='barbers.price'),
        ),
    ]
