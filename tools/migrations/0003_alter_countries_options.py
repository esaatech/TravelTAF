# Generated by Django 5.1.4 on 2025-01-15 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_countries_visatype_visarelationship'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countries',
            options={'ordering': ['name']},
        ),
    ]