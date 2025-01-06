# Generated by Django 5.1.4 on 2025-01-04 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='testimonial_type',
            field=models.CharField(choices=[('Express Entry PR', 'Express Entry PR'), ('Student Visa', 'Student Visa'), ('Work Visa', 'Work Visa'), ('Skilled Migration', 'Skilled Migration'), ('Tourism Package', 'Tourism Package'), ('Travel & Tours', 'Travel & Tours'), ('Holiday Package', 'Holiday Package'), ('Business Travel', 'Business Travel')], help_text='Type of service received', max_length=100),
        ),
    ]