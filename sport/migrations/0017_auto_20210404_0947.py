# Generated by Django 3.1.7 on 2021-04-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0016_remove_field_schedule_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='schedule_time',
            field=models.TimeField(default='00:00:00'),
        ),
    ]
