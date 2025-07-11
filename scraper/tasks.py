import logging

from celery import shared_task

from .models import Scraper, ScrapingTask
from .scrapers.linkedin_scraper import LinkedInPersonScraper

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def scrape_linkedin_profile_task(self, task_id, linkedin_url):
    """
    Celery task to scrape a LinkedIn profile asynchronously
    """
    # Update task status to STARTED
    try:
        task_record = ScrapingTask.objects.get(task_id=task_id)
        task_record.status = "STARTED"
        task_record.save()
    except ScrapingTask.DoesNotExist:
        logger.error(f"Task record not found for task_id: {task_id}")
        return

    try:
        # Check if we have scraper credentials
        if not Scraper.objects.exists():
            error_msg = "No scraper credentials found. Please contact support."
            task_record.status = "FAILURE"
            task_record.error_message = error_msg
            task_record.save()
            return {"success": False, "error": error_msg}

        # Initialize and run scraper
        scraper = LinkedInPersonScraper()
        person_data = scraper.scrape_person(linkedin_url)

        # Update task with success result
        result_data = {"success": True, "data": person_data}
        task_record.status = "SUCCESS"
        task_record.result = result_data
        task_record.save()

        logger.info(f"Successfully scraped LinkedIn profile: {linkedin_url}")
        return result_data

    except ValueError as e:
        # Handle validation errors
        error_msg = str(e)
        task_record.status = "FAILURE"
        task_record.error_message = error_msg
        task_record.save()

        logger.error(f"Validation error in LinkedIn scraping: {error_msg}")
        return {"success": False, "error": error_msg}

    except Exception as e:
        # Handle unexpected errors
        import traceback

        error_msg = f"Scraping failed: {str(e)}"
        full_traceback = traceback.format_exc()

        task_record.status = "FAILURE"
        task_record.error_message = error_msg
        task_record.save()

        logger.error(f"Unexpected error in LinkedIn profile scraping: {str(e)}")
        logger.error(f"Full traceback: {full_traceback}")
        return {"success": False, "error": error_msg}
