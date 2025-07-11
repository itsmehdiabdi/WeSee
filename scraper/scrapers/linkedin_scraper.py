from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
from scraper.models import Scraper
import logging

logger = logging.getLogger(__name__)

# Patch the focus method to handle missing alerts gracefully
def patched_focus(self):
    try:
        self.driver.execute_script('alert("Focus window")')
        self.driver.switch_to.alert.accept()
    except NoAlertPresentException:
        # Alert was blocked or auto-dismissed, just focus the window instead
        self.driver.switch_to.window(self.driver.current_window_handle)

# Apply the patch
from linkedin_scraper.objects import Scraper as LinkedInScraper
LinkedInScraper.focus = patched_focus


class LinkedInPersonScraper:
    def __init__(self):
        """
        Initialize LinkedIn scraper
        """
        self.driver = None
        
    def _setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
    
    def _get_credentials(self):
        """Get credentials from a random Scraper model"""
        # Use a random scraper
        scraper = Scraper.objects.order_by('?').first()
        if scraper:
            return scraper.email, scraper.password
        else:
            logger.error("No scraper credentials found in database")
            raise ValueError("No scraper credentials found in database")
    
    def scrape_person(self, linkedin_url):
        """
        Scrape a person's LinkedIn profile
        
        Args:
            linkedin_url: LinkedIn profile URL to scrape
            
        Returns:
            dict: Dictionary containing scraped person data
        """
        try:
            # Setup driver
            self.driver = self._setup_driver()
            
            # Get credentials
            email, password = self._get_credentials()
            
            # Login to LinkedIn
            logger.info("Logging into LinkedIn...")
            actions.login(self.driver, email, password)
            
            # Scrape person data
            logger.info(f"Scraping profile: {linkedin_url}")
            person = Person(linkedin_url, driver=self.driver)
            
            # Extract data
            person_data = {
                'name': person.name,
                'job_title': person.job_title,
                'company': person.company,
                'location': person.location,
                'about': person.about,
                'experiences': person.experiences,
                'educations': person.educations,
                'interests': person.interests,
                'accomplishments': person.accomplishments,
                'also_viewed_urls': person.also_viewed_urls,
                'contacts': person.contacts,
                'linkedin_url': person.linkedin_url,
            }
            
            logger.info(f"Successfully scraped profile for: {person.name}")
            return person_data
            
        except Exception as e:
            logger.error(f"Error scraping LinkedIn profile: {str(e)}")
            raise e
        finally:
            # Clean up
            if self.driver:
                self.driver.quit()
