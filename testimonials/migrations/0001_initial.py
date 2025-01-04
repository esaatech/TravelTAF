# Generated by Django 5.1.4 on 2025-01-04 13:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('initials', models.CharField(help_text='e.g., JD for John Davis', max_length=2)),
                ('location', models.CharField(help_text='e.g., Relocated to Canada', max_length=100)),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('testimonial_text', models.TextField()),
                ('testimonial_type', models.CharField(help_text='e.g., Express Entry PR', max_length=100)),
                ('duration', models.CharField(help_text='e.g., 6 months', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
                'ordering': ['-created_at'],
            },
        ),
    ]
