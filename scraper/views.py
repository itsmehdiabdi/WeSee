import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .scrapers.linkedin_scraper import LinkedInPersonScraper
from .models import Scraper
from .serializers import (
    LinkedInScrapeRequestSerializer,
    LinkedInScrapeResponseSerializer
)

logger = logging.getLogger(__name__)


class LinkedInProfileScrapeAPIView(APIView):
    """
    API endpoint to scrape a LinkedIn profile using DRF
    """
    permission_classes = [AllowAny]  # Adjust permissions as needed
    
    def post(self, request):
        """
        Scrape a LinkedIn profile
        
        Request body:
        {
            "linkedin_url": "https://www.linkedin.com/in/username/"
        }
        """
        # Validate request data
        request_serializer = LinkedInScrapeRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response({
                'success': False,
                'error': request_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = request_serializer.validated_data
        linkedin_url = validated_data['linkedin_url']
        
        try:
            # Check if we have scraper credentials
            if not Scraper.objects.exists():
                return Response({
                    'success': False,
                    'error': 'No scraper credentials found. Please create a Scraper instance first.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Initialize and run scraper
            scraper = LinkedInPersonScraper()
            person_data = scraper.scrape_person(linkedin_url)
            
            # Serialize response data
            response_data = {
                'success': True,
                'data': person_data
            }
            
            response_serializer = LinkedInScrapeResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
            else:
                # If response validation fails, still return the data but log the issue
                logger.warning(f"Response serialization failed: {response_serializer.errors}")
                return Response(response_data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in LinkedIn profile scraping: {str(e)}")
            return Response({
                'success': False,
                'error': f'Scraping failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Keep the original function as an alias for backward compatibility if needed
scrape_linkedin_profile = LinkedInProfileScrapeAPIView.as_view()
