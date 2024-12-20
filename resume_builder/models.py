from django.db import models
from django.contrib.auth import get_user_model

class Resume(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    personal_info = models.JSONField()  # Name, contact, location, etc.
    summary = models.TextField(blank=True)  # Professional summary
    work_experience = models.JSONField()  # List of work experiences
    education = models.JSONField()  # List of education entries
    skills = models.JSONField()  # Technical and soft skills
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_optimized = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"

    class Meta:
        ordering = ['-updated_at']
