from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class WhatsAppConversation(models.Model):
    customer_id = models.CharField(max_length=100)  # WhatsApp ID
    customer_name = models.CharField(max_length=255, blank=True)
    customer_phone = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('archived', 'Archived')
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"WhatsApp: {self.customer_name or self.customer_phone}"

    class Meta:
        ordering = ['-updated_at']

class WhatsAppMessage(models.Model):
    conversation = models.ForeignKey(
        WhatsAppConversation, 
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message_id = models.CharField(max_length=100, unique=True)
    direction = models.CharField(max_length=10, choices=[
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing')
    ])
    content = models.TextField()
    media_url = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('received', 'Received'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed')
    ])
    timestamp = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"WhatsApp {self.direction} message in {self.conversation}"

    class Meta:
        ordering = ['timestamp']

class WhatsAppQuickReply(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"WhatsApp Reply: {self.title}"

    class Meta:
        verbose_name = "WhatsApp Quick Reply"
        verbose_name_plural = "WhatsApp Quick Replies"