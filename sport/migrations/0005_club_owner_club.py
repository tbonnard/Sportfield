# Generated by Django 3.1.7 on 2021-03-30 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0004_auto_20210330_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='owner_club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='take_clubs_from_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
