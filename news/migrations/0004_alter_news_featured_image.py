# Generated by Django 5.1.4 on 2024-12-18 06:49

import storages.backends.gcloud
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_news_content_blocks_news_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.gcloud.GoogleCloudStorage(), upload_to='news_images/'),
        ),
    ]