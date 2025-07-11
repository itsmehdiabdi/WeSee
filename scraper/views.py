import logging
import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ScrapingTask
from .serializers import (
    LinkedInScrapeRequestSerializer,
    TaskCreatedResponseSerializer,
    TaskStatusResponseSerializer,
)
from .tasks import scrape_linkedin_profile_task

logger = logging.getLogger(__name__)

class LinkedInProfileScrapeAsyncAPIView(APIView):
    """
    API endpoint to scrape a LinkedIn profile asynchronously using Celery
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Start an async LinkedIn profile scraping task

        Request body:
        {
            "linkedin_url": "https://www.linkedin.com/in/username/"
        }
        
        Response:
        {
            "success": true,
            "task_id": "uuid",
            "message": "Task started successfully",
            "status_url": "/api/scrape/status/uuid/"
        }
        """
        # Validate request data
        request_serializer = LinkedInScrapeRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(
                {"success": False, "error": request_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = request_serializer.validated_data
        linkedin_url = validated_data["linkedin_url"]

        try:
            # Generate unique task ID
            task_id = str(uuid.uuid4())

            # Create task record in database
            task_record = ScrapingTask.objects.create(
                task_id=task_id,
                linkedin_url=linkedin_url,
                status='PENDING'
            )

            # Start the async task
            scrape_linkedin_profile_task.delay(task_id, linkedin_url)

            # Build status URL
            status_url = request.build_absolute_uri(
                reverse('scraper:task-status', kwargs={'task_id': task_id})
            )

            response_data = {
                "success": True,
                "task_id": task_id,
                "message": "Task started successfully",
                "status_url": status_url
            }

            response_serializer = TaskCreatedResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(
                    response_serializer.validated_data, status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(response_data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.error(f"Error starting async LinkedIn scraping task: {str(e)}")
            return Response(
                {"success": False, "error": f"Failed to start task: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TaskStatusAPIView(APIView):
    """
    API endpoint to check the status of a scraping task
    """

    permission_classes = [AllowAny]

    def get(self, request, task_id):
        """
        Get the status of a scraping task
        
        Response:
        {
            "task_id": "uuid",
            "status": "SUCCESS|PENDING|FAILURE|STARTED",
            "linkedin_url": "https://www.linkedin.com/in/username/",
            "created_at": "2023-...",
            "updated_at": "2023-...",
            "result": {...},  // Only present if status is SUCCESS
            "error_message": "..."  // Only present if status is FAILURE
        }
        """
        try:
            task_record = ScrapingTask.objects.get(task_id=task_id)
        except ScrapingTask.DoesNotExist:
            return Response(
                {"success": False, "error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        response_data = {
            "task_id": task_record.task_id,
            "status": task_record.status,
            "linkedin_url": task_record.linkedin_url,
            "created_at": task_record.created_at,
            "updated_at": task_record.updated_at,
        }

        # Add result if available
        if task_record.result:
            response_data["result"] = task_record.result

        # Add error message if failed
        if task_record.error_message:
            response_data["error_message"] = task_record.error_message

        response_serializer = TaskStatusResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(
                response_serializer.validated_data, status=status.HTTP_200_OK
            )
        else:
            return Response(response_data, status=status.HTTP_200_OK)
