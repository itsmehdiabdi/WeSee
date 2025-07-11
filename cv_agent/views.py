import uuid
import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from users.utils import user_exists_in_db
from .models import CVTask
from .tasks import create_cv_task

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_cv_view(request):
    """
    Create a CV task for a given LinkedIn URL and job description.
    
    Expected payload:
    {
        "linkedin_url": "https://linkedin.com/in/username",
        "job_description": "Job description text..."
    }
    """
    linkedin_url = request.data.get('linkedin_url')
    job_description = request.data.get('job_description')
    
    # Validate required fields
    if not linkedin_url:
        return Response(
            {"error": "linkedin_url is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not job_description:
        return Response(
            {"error": "job_description is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if LinkedIn data exists in database
    if not user_exists_in_db(linkedin_url):
        return Response(
            {
                "error": f"LinkedIn data not found for URL: {linkedin_url}. "
                         "Please scrape the profile first."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create CV task record
        cv_task = CVTask.objects.create(
            task_id=task_id,
            linkedin_url=linkedin_url,
            job_description=job_description,
            status="PENDING"
        )
        
        # Start the Celery task
        create_cv_task.delay(task_id, linkedin_url, job_description)
        
        logger.info(f"Created CV task {task_id} for LinkedIn URL: {linkedin_url}")
        
        return Response(
            {
                "task_id": task_id,
                "status": "PENDING",
                "message": "CV creation task started successfully"
            },
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        logger.error(f"Error creating CV task: {str(e)}")
        return Response(
            {"error": f"Failed to create CV task: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_cv_task_status(request, task_id):
    """
    Get the status and result of a CV task.
    """
    try:
        cv_task = CVTask.objects.get(task_id=task_id)
        
        response_data = {
            "task_id": task_id,
            "status": cv_task.status,
            "linkedin_url": cv_task.linkedin_url,
            "created_at": cv_task.created_at,
            "updated_at": cv_task.updated_at,
        }
        
        if cv_task.status == "SUCCESS" and cv_task.result:
            response_data["cv_content"] = cv_task.result
        elif cv_task.status == "FAILURE" and cv_task.error_message:
            response_data["error"] = cv_task.error_message
            
        return Response(response_data, status=status.HTTP_200_OK)
        
    except CVTask.DoesNotExist:
        return Response(
            {"error": f"CV task with ID {task_id} not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error retrieving CV task status: {str(e)}")
        return Response(
            {"error": f"Failed to retrieve task status: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
