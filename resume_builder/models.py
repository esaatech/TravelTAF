from django.db import models
from django.contrib.auth import get_user_model

class Resume(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Content fields
    original_content = models.TextField()
    optimized_content = models.TextField()
    job_description = models.TextField()
    
    # Optimization results
    keyword_matches = models.JSONField(default=list)
    improvement_suggestions = models.JSONField(default=list)
    ats_score = models.IntegerField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Resume for {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
