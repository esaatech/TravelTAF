from django.db import models

class Countries(models.Model):
    name = models.CharField(max_length=100)
    iso_code_2 = models.CharField(max_length=2, unique=True)
    iso_code_3 = models.CharField(max_length=3, unique=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    continent = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



