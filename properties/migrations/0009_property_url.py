# Generated by Django 5.0.4 on 2024-04-27 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_remove_direction_direction_direction_route_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='URL'),
        ),
    ]
