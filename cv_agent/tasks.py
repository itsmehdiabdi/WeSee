import logging
from celery import shared_task

from users.utils import get_user_data_by_linkedin_url
from .models import CVTask
from .services.wesee.main import run

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def create_cv_task(self, task_id, linkedin_url, job_description):
    """
    Celery task to create a customized CV using the WeSee crew
    """
    # Update task status to STARTED
    try:
        task_record = CVTask.objects.get(task_id=task_id)
        task_record.status = "STARTED"
        task_record.save()
    except CVTask.DoesNotExist:
        logger.error(f"CV Task record not found for task_id: {task_id}")
        return

    try:
        # Get LinkedIn data from database
        linkedin_data = get_user_data_by_linkedin_url(linkedin_url)
        if not linkedin_data:
            error_msg = f"Failed to retrieve LinkedIn data for URL: {linkedin_url}"
            task_record.status = "FAILURE"
            task_record.error_message = error_msg
            task_record.save()
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        logger.info(f"Retrieved LinkedIn data for {linkedin_url}, running CV creation crew...")

        # Run the WeSee crew to create the CV
        result = run(linkedin_data, job_description)
        
        # Extract the CV content from the result
        if hasattr(result, 'raw') and result.raw:
            cv_content = result.raw
        elif hasattr(result, 'content') and result.content:
            cv_content = result.content
        else:
            cv_content = str(result)

        # Update task with success result
        task_record.status = "SUCCESS"
        task_record.result = cv_content
        task_record.save()

        logger.info(f"Successfully created CV for LinkedIn profile: {linkedin_url}")
        return {"success": True, "cv_content": cv_content}

    except Exception as e:
        # Handle unexpected errors
        import traceback

        error_msg = f"CV creation failed: {str(e)}"
        full_traceback = traceback.format_exc()

        task_record.status = "FAILURE"
        task_record.error_message = error_msg
        task_record.save()

        logger.error(f"Unexpected error in CV creation: {str(e)}")
        logger.error(f"Full traceback: {full_traceback}")
        return {"success": False, "error": error_msg} 
