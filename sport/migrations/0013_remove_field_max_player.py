# Generated by Django 3.1.7 on 2021-04-02 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0012_auto_20210331_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='max_player',
        ),
    ]
