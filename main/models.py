from django.db import models
import uuid
from django.utils.text import slugify

# Create your models here.
class VacationSearch(models.Model):
    # User and Search Info
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    search_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Search Parameters
    destination = models.CharField(max_length=255)
    travel_dates = models.JSONField()  # Store date range
    budget_range = models.CharField(max_length=50)
    travelers = models.IntegerField()
    
    # API Response Data
    search_results = models.JSONField()  # Store complete API response
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['search_id']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Search for {self.destination} on {self.created_at.date()}"

class TravelDestination(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True, help_text="Two-letter country code (e.g., 'CA' for Canada)")
    flag = models.ImageField(upload_to='destination_flags/', help_text="Destination flag image")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show this destination in the featured section")
    order = models.PositiveIntegerField(default=0, help_text="Order in which to display the destination")
    
    # Key features/attractions
    feature1_icon = models.CharField(max_length=50, help_text="SVG path or icon class")
    feature1_text = models.CharField(max_length=100)
    feature2_icon = models.CharField(max_length=50, help_text="SVG path or icon class")
    feature2_text = models.CharField(max_length=100)
    feature3_icon = models.CharField(max_length=50, help_text="SVG path or icon class")
    feature3_text = models.CharField(max_length=100)
    
    # Meta information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Travel Destination"
        verbose_name_plural = "Travel Destinations"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only a limited number of destinations are featured
        if self.is_featured:
            featured_count = TravelDestination.objects.filter(is_featured=True).exclude(pk=self.pk).count()
            if featured_count >= 3:  # Limit to 3 featured destinations
                self.is_featured = False
        super().save(*args, **kwargs)