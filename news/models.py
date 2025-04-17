from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import JSONField
from django_ckeditor_5.fields import CKEditor5Field
from django.core.files.storage import default_storage
from storages.backends.gcloud import GoogleCloudStorage
from .services.pubsub import NewsletterPublisher
import logging
import asyncio

logger = logging.getLogger(__name__)

# Initialize GCS storage
gcs_storage = GoogleCloudStorage()

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class News(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news')
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    send_as_newsletter = models.BooleanField(
        default=False,
        help_text="If checked, this article will be included in the next newsletter"
    )
    
    featured_image = models.ImageField(
        upload_to='news_images/',
        storage=gcs_storage,  # Force using GCS storage
        null=True,
        blank=True
    )
    summary = models.TextField(help_text="A brief introduction or summary of the article",blank=True)
    content = CKEditor5Field('Content', config_name='default')
    source_name = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(blank=True)

    # Add new status management fields
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
        related_name='approved_news'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True, help_text="Feedback for rejected articles")

    class Meta:
        verbose_name_plural = "News Articles"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def delete_image(self):
        """Delete the image from GCS bucket"""
        if self.featured_image:
            logger.info(f"Deleting image: {self.featured_image.name}")
            try:
                # Delete the file from GCS
                self.featured_image.storage.delete(self.featured_image.name)
                logger.info(f"Successfully deleted image from GCS")
            except Exception as e:
                logger.error(f"Error deleting image from GCS: {str(e)}")
                raise

    def save(self, *args, **kwargs):
        # Store the old instance if this is an update
        if self.pk:
            try:
                old_instance = News.objects.get(pk=self.pk)
                old_send_as_newsletter = old_instance.send_as_newsletter
                
                # Handle image changes
                if old_instance.featured_image and (not self.featured_image or 
                   old_instance.featured_image != self.featured_image):
                    old_instance.delete_image()
                    logger.info("Old image deleted successfully")
            except News.DoesNotExist:
                old_send_as_newsletter = False
            except Exception as e:
                logger.error(f"Error handling old image: {str(e)}")
                old_send_as_newsletter = False
        else:
            old_send_as_newsletter = False

        # Save the model first
        super().save(*args, **kwargs)

        # Handle newsletter publishing if the flag is newly set to True
        try:
            if self.send_as_newsletter and not old_send_as_newsletter:
                publisher = NewsletterPublisher()
                publisher.publish_newsletter_sync(self)
                logger.info(f"Successfully queued news article {self.id} for newsletter")
        except Exception as e:
            logger.error(f"Failed to publish newsletter for news article {self.id}: {str(e)}")
            # Note: We're not raising the exception here to prevent save failure
            # but you might want to handle this differently based on your requirements

    def delete(self, *args, **kwargs):
        """Override delete to clean up files"""
        # Delete the image first
        self.delete_image()
        # Then delete the model instance
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})

class DialogContent(models.Model):
    title = models.CharField(max_length=255, default="Stay Updated with Our Latest News")
    body = models.TextField(default="Subscribe to our newsletter and never miss important updates!")
    news = models.OneToOneField('News', on_delete=models.CASCADE, related_name='dialog_content')

    def __str__(self):
        return f"Dialog for {self.news.title}"
