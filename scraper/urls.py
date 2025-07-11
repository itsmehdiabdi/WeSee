from django.urls import path

from .views import LinkedInProfileScrapeAsyncAPIView, TaskStatusAPIView

app_name = "scraper"

urlpatterns = [
    # Asynchronous scraping
    path(
        "",
        LinkedInProfileScrapeAsyncAPIView.as_view(),
        name="linkedin-scrape-async",
    ),
    # Task status checking
    path(
        "status/<str:task_id>/",
        TaskStatusAPIView.as_view(),
        name="task-status",
    ),
]
