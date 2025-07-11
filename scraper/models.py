from django.db import models


# Create your models here.
class Scraper(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ScrapingTask(models.Model):
    TASK_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('STARTED', 'Started'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]
    
    task_id = models.CharField(max_length=255, unique=True)
    linkedin_url = models.URLField()
    status = models.CharField(max_length=10, choices=TASK_STATUS_CHOICES, default='PENDING')
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Task {self.task_id} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
