from django.db import models
import uuid
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