# Generated by Django 5.0.4 on 2024-04-27 16:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0011_alter_property_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('avenue', 'Avenida'), ('gated_community', 'Condominio Cerrado'), ('asphalt', 'Asfalto'), ('dirt_road', 'Dirt Road')]), blank=True, default=list, size=None, verbose_name='Etiquetas'),
        ),
    ]
