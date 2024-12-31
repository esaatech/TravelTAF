# promotions/models.py
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.urls import NoReverseMatch


class PromotionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    
    # Link handling
    link_type = models.CharField(
        max_length=10, 
        choices=[
            ('internal', 'Internal Link'),
            ('external', 'External URL'),
        ], 
        default='internal'
    )
    external_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Use this for external links (e.g., https://example.com)"
    )
    internal_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text=(
            "Name of the URL pattern (e.g., 'tools:school_finder', 'news:detail'). "
            "You can find this in your urls.py files as the 'name' parameter."
        )
    )
    
    # Promotion type as ForeignKey
    promotion_type = models.ForeignKey(
        PromotionType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='promotions'
    )
    
    # Call to action
    cta_text = models.CharField(
        max_length=50, 
        default="Learn More",
        help_text="Text to display on the call-to-action button"
    )
    
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
        if self.link_type == 'external' and self.external_url:
            return self.external_url
        elif self.link_type == 'internal' and self.internal_name:
            try:
                return reverse(self.internal_name)
            except NoReverseMatch:
                return '#'  # Fallback to hash if URL pattern not found
        return '#'  # Default fallback

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True