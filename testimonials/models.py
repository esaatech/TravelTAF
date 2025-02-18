from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Testimonial(models.Model):
    SERVICE_CHOICES = [
        ('Express Entry PR', 'Express Entry PR'),
        ('Student Visa', 'Student Visa'),
        ('Work Visa', 'Work Visa'),
        ('Skilled Migration', 'Skilled Migration'),
        ('Tourism Package', 'Tourism Package'),
        ('Travel & Tours', 'Travel & Tours'),
        ('Holiday Package', 'Holiday Package'),
        ('Business Travel', 'Business Travel'),
    ]

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=2, help_text="e.g., JD for John Davis")
    location = models.CharField(max_length=100, help_text="e.g., Relocated to Canada")
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    testimonial_text = models.TextField()
    testimonial_type = models.CharField(
        max_length=100,
        choices=SERVICE_CHOICES,
        help_text="Type of service received"
    )
    duration = models.CharField(max_length=50, help_text="e.g., 6 months")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} - {self.testimonial_type}"

    def get_absolute_url(self):
        return reverse('testimonials:testimonial_list')
