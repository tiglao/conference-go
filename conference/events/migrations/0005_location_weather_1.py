# Generated by Django 4.0.3 on 2023-06-23 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_location_weather'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='weather_1',
            field=models.TextField(null=True),
        ),
    ]