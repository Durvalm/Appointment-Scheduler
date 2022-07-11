# Generated by Django 4.0.6 on 2022-07-11 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('barbers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('barbers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='barbers.barber')),
            ],
        ),
    ]