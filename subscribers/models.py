from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
    SUBSCRIPTION_TYPES = [
        ('newsletter', 'General Newsletter'),
        ('news', 'News Updates'),
    ]

    email = models.EmailField(unique=True)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='newsletter')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.get_subscription_type_display()}"

    class Meta:
        ordering = ['-created_at']
