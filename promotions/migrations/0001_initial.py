# Generated by Django 5.1.4 on 2024-12-31 15:34

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='promotions/')),
                ('link_type', models.CharField(choices=[('internal', 'Internal Link'), ('external', 'External URL')], default='internal', max_length=10)),
                ('external_url', models.URLField(blank=True, help_text='Use this for external links', null=True)),
                ('internal_name', models.CharField(blank=True, help_text='Name of the internal URL pattern', max_length=100, null=True)),
                ('cta_text', models.CharField(default='Learn More', help_text='Text to display on the call-to-action button', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0, help_text='Lower numbers will be displayed first')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('promotion_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promotions', to='promotions.promotiontype')),
            ],
            options={
                'verbose_name': 'Promotion',
                'verbose_name_plural': 'Promotions',
                'ordering': ['order', '-start_date'],
            },
        ),
    ]