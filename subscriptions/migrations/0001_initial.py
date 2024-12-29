# Generated by Django 5.1.4 on 2024-12-29 18:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureCatalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('identifier', models.SlugField(help_text='Unique identifier used in code to reference this feature', max_length=100, unique=True)),
                ('type', models.CharField(choices=[('TOOL', 'Tool'), ('SERVICE', 'Service')], help_text='Whether this is a tool or service', max_length=10)),
                ('description', models.TextField(help_text='Detailed description of what this feature provides')),
            ],
            options={
                'verbose_name': 'Feature',
                'verbose_name_plural': 'Features',
                'ordering': ['type', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('duration_type', models.CharField(choices=[('ONE_TIME', 'One Time'), ('MONTHLY', 'Monthly'), ('QUARTERLY', 'Quarterly'), ('SEMI_ANNUAL', 'Semi-Annual'), ('YEARLY', 'Yearly')], default='MONTHLY', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, help_text='Price in USD', max_digits=10)),
                ('has_full_access', models.BooleanField(default=False, help_text='If True, this plan has access to all features regardless of selection')),
                ('stripe_price_id', models.CharField(blank=True, help_text='Stripe Price ID for this plan', max_length=100)),
                ('features', models.ManyToManyField(blank=True, help_text='Features included in this plan (ignored if has_full_access is True)', to='subscriptions.featurecatalog')),
            ],
            options={
                'verbose_name': 'Subscription Plan',
                'verbose_name_plural': 'Subscription Plans',
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('EXPIRED', 'Expired'), ('CANCELLED', 'Cancelled'), ('PENDING', 'Pending')], default='PENDING', max_length=10)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('stripe_subscription_id', models.CharField(blank=True, help_text='Stripe Subscription ID for recurring subscriptions', max_length=100)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_subscriptions', to='subscriptions.subscriptionplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Subscription',
                'verbose_name_plural': 'User Subscriptions',
                'ordering': ['-created_at'],
            },
        ),
    ]
