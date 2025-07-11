from django.urls import path

from .views import LinkedInProfileScrapeAPIView

app_name = "scraper"

urlpatterns = [
    path(
        "",
        LinkedInProfileScrapeAPIView.as_view(),
        name="linkedin-scrape",
    ),
]
