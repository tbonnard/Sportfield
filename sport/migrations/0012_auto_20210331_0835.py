# Generated by Django 3.1.7 on 2021-03-31 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0011_auto_20210330_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('date_book', models.DateField()),
                ('hour_book', models.TimeField()),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='take_Booking_from_field', to='sport.field')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='take_Booking_from_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
    ]