# promotions/models.py
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Promotion(models.Model):
    LINK_TYPE_CHOICES = [
        ('internal', 'Internal Link'),
        ('external', 'External URL'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    
    # Link handling
    link_type = models.CharField(max_length=10, choices=LINK_TYPE_CHOICES, default='internal')
    external_url = models.URLField(blank=True, null=True, 
                                 help_text="Use this for external links")
    internal_name = models.CharField(max_length=100, blank=True, null=True,
                                   help_text="Name of the internal URL pattern")
    
    # Display control
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0,
                              help_text="Lower numbers will be displayed first")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.link_type == 'external':
            return self.external_url
        return reverse(self.internal_name)

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True