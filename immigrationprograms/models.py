from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.conf import settings
from tools.models import Countries  # Import Country model from tools app
from django.urls import reverse

class ImmigrationProgram(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    country = models.ForeignKey(
        Countries, 
        on_delete=models.CASCADE,
        related_name='immigration_programs'  # This creates the reverse relationship
    )
    description = CKEditor5Field('Description', config_name='default')
    eligibility_criteria = CKEditor5Field('Eligibility Criteria', config_name='default')
    benefits = CKEditor5Field('Benefits', config_name='default')
    application_process = CKEditor5Field('Application Process', config_name='default')
    
    featured_image = models.ImageField(
        upload_to='immigration_images/',
        storage=settings.DEFAULT_FILE_STORAGE,
        null=True,
        blank=True
    )
    
    deadline = models.DateField(null=True, blank=True)
    official_link = models.URLField(blank=True, null=True)
    chat_enabled = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    # Status management fields
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    approved_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_programs'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True, help_text="Feedback for rejected programs")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Immigration Programs"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('immigration:program_detail', kwargs={
            'country_slug': self.country.iso_code_2.lower(),
            'program_slug': self.slug
        })

class FeaturedCountry(models.Model):
    country = models.ForeignKey(
        Countries,  # Use the imported Countries model
        on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Featured Country'
        verbose_name_plural = 'Featured Countries'

    def __str__(self):
        return f"{self.country.name}"