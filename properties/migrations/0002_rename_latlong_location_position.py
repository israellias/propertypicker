# Generated by Django 5.0.4 on 2024-04-26 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='latlong',
            new_name='position',
        ),
    ]
