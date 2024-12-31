# Generated by Django 5.1.4 on 2024-12-30 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='credittransaction',
            name='currency',
            field=models.CharField(default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='credittransaction',
            name='payment_intent_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]