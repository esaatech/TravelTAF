# Generated by Django 5.1.4 on 2024-12-31 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_usersubscription_stripe_payment_intent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='invoice_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='stripe_invoice_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
