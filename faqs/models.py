from django.db import models

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Questions'),
        ('services', 'Our Services'),
        ('pricing', 'Pricing & Payment'),
        ('process', 'Process & Timeline'),
        ('support', 'Support'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question
