from django.db import models
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from django.utils import timezone

gcs_storage = GoogleCloudStorage()

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    pdf_file = models.FileField(
        upload_to=lambda instance, filename: f'resumes/{instance.user.id}/resume.pdf',
        storage=gcs_storage,  # Force using GCS storage
        null=True,
        blank=True
    )
    template_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Content fields with default values
    original_content = models.TextField(default='')
    optimized_content = models.TextField(default='')
    job_description = models.TextField(default='')
    
    # Optimization results with default values
    keyword_matches = models.JSONField(default=list)
    improvement_suggestions = models.JSONField(default=list)
    ats_score = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Resume for {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        # If this is an update and there's an existing file, delete it
        if self.pk:
            try:
                old_instance = Resume.objects.get(pk=self.pk)
                if old_instance.pdf_file and self.pdf_file != old_instance.pdf_file:
                    old_instance.pdf_file.delete(save=False)
            except Resume.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the file when the model instance is deleted
        if self.pdf_file:
            self.pdf_file.delete(save=False)
        super().delete(*args, **kwargs)
