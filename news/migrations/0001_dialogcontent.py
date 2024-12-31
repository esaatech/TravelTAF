# Generated by Django 5.1.4 on 2024-12-26 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', 'XXXX_add_status_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialogContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Stay Updated with Our Latest News', max_length=255)),
                ('body', models.TextField(default='Subscribe to our newsletter and never miss important updates!')),
                ('news', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dialog_content', to='news.news')),
            ],
        ),
    ]