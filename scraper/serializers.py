from rest_framework import serializers


class LinkedInScrapeRequestSerializer(serializers.Serializer):
    """Serializer for LinkedIn scrape request data"""

    linkedin_url = serializers.URLField(
        required=True, help_text="LinkedIn profile URL to scrape"
    )
    scraper_id = serializers.IntegerField(
        required=False, help_text="ID of the Scraper instance to use (optional)"
    )

    def validate_linkedin_url(self, value):
        """Validate that the URL is a LinkedIn profile URL"""
        if "linkedin.com/in/" not in value:
            raise serializers.ValidationError(
                "Must be a valid LinkedIn profile URL (containing 'linkedin.com/in/')"
            )
        return value


class ExperienceSerializer(serializers.Serializer):
    """Serializer for experience data"""

    institution_name = serializers.CharField(required=False, allow_blank=True)
    website = serializers.CharField(required=False, allow_blank=True)
    degree = serializers.CharField(required=False, allow_blank=True)
    date_range = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)


class EducationSerializer(serializers.Serializer):
    """Serializer for education data"""

    institution_name = serializers.CharField(required=False, allow_blank=True)
    website = serializers.CharField(required=False, allow_blank=True)
    degree = serializers.CharField(required=False, allow_blank=True)
    date_range = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)


class ContactSerializer(serializers.Serializer):
    """Serializer for contact information"""

    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)


class LinkedInPersonDataSerializer(serializers.Serializer):
    """Serializer for LinkedIn person data response"""

    name = serializers.CharField(required=False, allow_blank=True)
    job_title = serializers.CharField(required=False, allow_blank=True)
    company = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    about = serializers.CharField(required=False, allow_blank=True)
    experiences = ExperienceSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)
    interests = serializers.ListField(child=serializers.CharField(), required=False)
    accomplishments = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    also_viewed_urls = serializers.ListField(
        child=serializers.URLField(), required=False
    )
    contacts = ContactSerializer(required=False)
    linkedin_url = serializers.URLField(required=False, allow_blank=True)


class LinkedInScrapeResponseSerializer(serializers.Serializer):
    """Serializer for the complete LinkedIn scrape response"""

    success = serializers.BooleanField()
    data = LinkedInPersonDataSerializer(required=False)
    error = serializers.CharField(required=False, allow_blank=True)


class TaskCreatedResponseSerializer(serializers.Serializer):
    """Serializer for async task creation response"""

    success = serializers.BooleanField()
    task_id = serializers.CharField()
    message = serializers.CharField()
    status_url = serializers.URLField()


class TaskStatusResponseSerializer(serializers.Serializer):
    """Serializer for task status response"""

    task_id = serializers.CharField()
    status = serializers.CharField()
    linkedin_url = serializers.URLField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    result = serializers.JSONField(required=False)
    error_message = serializers.CharField(required=False, allow_blank=True)
