# Generated by Django 3.1.7 on 2021-03-30 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0005_club_owner_club'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='Category',
            new_name='category',
        ),
    ]
