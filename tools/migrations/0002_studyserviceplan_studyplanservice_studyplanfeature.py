# Generated by Django 5.1.4 on 2024-12-29 16:27

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyServicePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('plan_type', models.CharField(choices=[('program_support', 'Program Application Support'), ('study_abroad', 'Complete Study Abroad Service')], max_length=50, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('timeline', models.CharField(max_length=100)),
                ('button_text', models.CharField(max_length=50)),
                ('button_url', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Study Service Plan',
                'verbose_name_plural': 'Study Service Plans',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='StudyPlanService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=255)),
                ('is_highlighted', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='included_services', to='tools.studyserviceplan')),
            ],
            options={
                'verbose_name': 'Included Service',
                'verbose_name_plural': 'Included Services',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='StudyPlanFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=255)),
                ('is_highlighted', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='tools.studyserviceplan')),
            ],
            options={
                'verbose_name': 'Plan Feature',
                'verbose_name_plural': 'Plan Features',
                'ordering': ['order'],
            },
        ),
    ]
