# Generated by Django 5.0.4 on 2024-04-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_property_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Nombre')),
            ],
        ),
    ]
