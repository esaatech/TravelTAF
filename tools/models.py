from django.db import models
from django.core.validators import MinValueValidator
from storages.backends.gcloud import GoogleCloudStorage

gcs_storage = GoogleCloudStorage()

def school_logo_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    
    # If this is a new school (no id yet), use a temporary path
    if instance.id is None:
        return f'schools/logos/temp/{filename}'
    
    # For existing schools, use their ID in the path
    return f'schools/logos/{instance.id}/logo.{ext}'

class ProgramLevel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Fields of Study"

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Countries"

class School(models.Model):
    # Basic Information
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name='schools',
        db_index=True
    )
    logo = models.ImageField(
        upload_to=school_logo_path,
        storage=gcs_storage,
        null=True, 
        blank=True
    )
    website = models.URLField()
    ranking = models.CharField(max_length=100)
    tuition = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    # Feature Flags
    scholarships_available = models.BooleanField(default=False)
    work_opportunities = models.BooleanField(default=False)
    housing_available = models.BooleanField(default=False)

    # Relations
    programs = models.ManyToManyField(ProgramLevel)
    fields_of_study = models.ManyToManyField(FieldOfStudy)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.country})"

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['tuition']),
        ]
