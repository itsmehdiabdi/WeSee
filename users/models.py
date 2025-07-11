from django.db import models


class User(models.Model):
    """
    Model to store LinkedIn user profile information
    """

    name = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    linkedin_url = models.URLField(unique=True)  # This will be our primary identifier

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.linkedin_url})"

    class Meta:
        ordering = ["-created_at"]


class Experience(models.Model):
    """
    Model to store work experience information
    """

    user = models.ForeignKey(User, related_name="experiences", on_delete=models.CASCADE)

    institution_name = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)
    company_size = models.CharField(max_length=100, null=True, blank=True)
    founded = models.CharField(max_length=100, null=True, blank=True)

    position_title = models.CharField(max_length=255, null=True, blank=True)
    from_date = models.CharField(max_length=100, null=True, blank=True)
    to_date = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position_title} at {self.institution_name}"

    class Meta:
        ordering = ["-created_at"]


class Education(models.Model):
    """
    Model to store education information
    """

    user = models.ForeignKey(User, related_name="educations", on_delete=models.CASCADE)

    institution_name = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)
    company_size = models.CharField(max_length=100, null=True, blank=True)
    founded = models.CharField(max_length=100, null=True, blank=True)

    degree = models.CharField(max_length=255, null=True, blank=True)
    from_date = models.CharField(max_length=100, null=True, blank=True)
    to_date = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.degree} from {self.institution_name}"

    class Meta:
        ordering = ["-created_at"]


class Interest(models.Model):
    """
    Model to store user interests (if any)
    """

    user = models.ForeignKey(User, related_name="interests", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Accomplishment(models.Model):
    """
    Model to store user accomplishments (if any)
    """

    user = models.ForeignKey(
        User, related_name="accomplishments", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
