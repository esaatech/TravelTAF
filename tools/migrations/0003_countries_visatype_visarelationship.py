# Generated by Django 5.1.4 on 2025-01-08 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_studyserviceplan_studyplanservice_studyplanfeature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('iso_code_2', models.CharField(max_length=2, unique=True)),
                ('iso_code_3', models.CharField(max_length=3, unique=True)),
                ('region', models.CharField(blank=True, max_length=50, null=True)),
                ('continent', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisaRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_stay_days', models.IntegerField(blank=True, null=True)),
                ('multiple_entry', models.BooleanField(default=False)),
                ('processing_time_days', models.IntegerField(blank=True, null=True)),
                ('fee_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fee_currency', models.CharField(blank=True, max_length=3, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('documents_required', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_until', models.DateField(blank=True, null=True)),
                ('last_verified_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visa_from_relationships', to='tools.countries')),
                ('to_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visa_to_relationships', to='tools.country')),
                ('visa_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.visatype')),
            ],
            options={
                'unique_together': {('from_country', 'to_country')},
            },
        ),
    ]
