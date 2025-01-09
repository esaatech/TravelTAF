# Generated by Django 5.1.4 on 2025-01-08 22:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_countries_visatype_visarelationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visarelationship',
            name='to_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visa_to_relationships', to='tools.countries'),
        ),
    ]
