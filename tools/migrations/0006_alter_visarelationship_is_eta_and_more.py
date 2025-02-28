# Generated by Django 5.1.4 on 2025-01-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0005_alter_visarelationship_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visarelationship',
            name='is_eta',
            field=models.BooleanField(default=False, help_text='Check if this requires ETA/eVisa', verbose_name='ETA/eVisa'),
        ),
        migrations.AlterField(
            model_name='visarelationship',
            name='is_visa_free',
            field=models.BooleanField(default=False, help_text='Check if this is a visa-free arrangement', verbose_name='Visa Free'),
        ),
    ]
