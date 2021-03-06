# Generated by Django 3.1.7 on 2021-03-30 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0002_user_admin_pro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=250)),
                ('image_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('address_number', models.IntegerField()),
                ('city', models.CharField(max_length=250)),
                ('zip_code', models.CharField(max_length=20)),
                ('country', models.CharField(choices=[('CA', 'Canada'), ('USA', 'United States of America')], max_length=3)),
                ('image_url', models.URLField()),
                ('Category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='take_clubs_from_category', to='sport.category')),
            ],
        ),
    ]
