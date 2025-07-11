from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import sys
import os
import json

# Add the Django project root to the Python path
# This allows us to import Django models and utilities
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../..'))
sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeSee.settings')
import django
django.setup()

from users.utils import get_user_data_by_linkedin_url


class LinkedInDataFetcherInput(BaseModel):
    """Input schema for LinkedIn Data Fetcher Tool."""
    linkedin_url: str = Field(
        ..., 
        description="The LinkedIn profile URL to fetch data for (e.g., 'https://www.linkedin.com/in/username/')"
    )


class LinkedInDataFetcher(BaseTool):
    name: str = "LinkedIn Data Fetcher"
    description: str = (
        "Fetches comprehensive LinkedIn profile data from the database using a LinkedIn URL. "
        "Returns structured data including personal information, work experiences, education, "
        "interests, and accomplishments. Use this tool when you need to retrieve stored "
        "LinkedIn profile data for analysis or CV generation."
    )
    args_schema: Type[BaseModel] = LinkedInDataFetcherInput

    def _run(self, linkedin_url: str) -> str:
        """
        Fetch LinkedIn data from database using the provided LinkedIn URL.
        
        Args:
            linkedin_url (str): The LinkedIn profile URL
            
        Returns:
            str: JSON string containing the LinkedIn profile data or error message
        """
        try:
            # Clean up the URL (remove trailing slashes, ensure proper format)
            linkedin_url = linkedin_url.strip().rstrip('/')
            
            # Validate that it's a LinkedIn URL
            if "linkedin.com/in/" not in linkedin_url:
                return json.dumps({
                    "error": "Invalid LinkedIn URL. Must contain 'linkedin.com/in/'",
                    "linkedin_url": linkedin_url
                })
            
            # Fetch user data from database
            user_data = get_user_data_by_linkedin_url(linkedin_url)
            
            if user_data is None:
                return json.dumps({
                    "error": "No data found for this LinkedIn URL in the database",
                    "linkedin_url": linkedin_url,
                    "suggestion": "The profile may need to be scraped first before it can be retrieved"
                })
            
            # Return the complete user data as JSON
            return json.dumps({
                "success": True,
                "linkedin_url": linkedin_url,
                "data": user_data
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": f"An error occurred while fetching LinkedIn data: {str(e)}",
                "linkedin_url": linkedin_url
            })
