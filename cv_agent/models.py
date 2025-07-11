from django.db import models

# Create your models here.


class CVTask(models.Model):
    TASK_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("STARTED", "Started"),
        ("SUCCESS", "Success"),
        ("FAILURE", "Failure"),
    ]

    task_id = models.CharField(max_length=255, unique=True)
    linkedin_url = models.URLField()
    job_description = models.TextField()
    status = models.CharField(
        max_length=10, choices=TASK_STATUS_CHOICES, default="PENDING"
    )
    result = models.TextField(null=True, blank=True)  # Store the generated CV
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CV Task {self.task_id} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
