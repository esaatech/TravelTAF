from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import JSONField

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
    
    featured_image = models.ImageField(upload_to='news_images/featured/', null=True, blank=True)
    summary = models.TextField(help_text="A brief introduction or summary of the article",blank=True)
    content_blocks = JSONField(default=list, help_text="Structured content blocks")
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
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
