# Generated by Django 4.0.6 on 2022-07-21 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('barbers', '0008_schedule_date_alter_schedule_time'),
        ('saloons', '0004_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbers.barber')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saloons.saloon')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbers.schedule')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbers.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
