# Generated by Django 4.0.6 on 2022-07-21 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barbers', '0008_schedule_date_alter_schedule_time'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('saloons', '0005_appointments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, null=True)),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbers.barber')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saloons.saloon')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbers.schedule')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbers.service')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Appointments',
        ),
    ]
