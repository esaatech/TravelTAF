from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import JSONField
from django_ckeditor_5.fields import CKEditor5Field
from django.core.files.storage import default_storage
from storages.backends.gcloud import GoogleCloudStorage
import logging

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
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news')
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
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

    class Meta:
        verbose_name_plural = "News Articles"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.featured_image:
            logger.info("=== Starting image upload ===")
            logger.info(f"Image name: {self.featured_image.name}")
            logger.info(f"Storage backend: {self.featured_image.storage.__class__.__name__}")
            
            try:
                super().save(*args, **kwargs)
                logger.info(f"Image saved successfully")
                logger.info(f"Image URL: {self.featured_image.url}")
            except Exception as e:
                logger.error(f"Upload failed: {str(e)}")
                logger.error(f"Storage details: {vars(self.featured_image.storage)}")
                raise
            
            logger.info("=== Upload process completed ===")
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
