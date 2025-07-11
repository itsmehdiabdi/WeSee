from django.contrib import admin

from .models import Scraper


@admin.register(Scraper)
class ScraperAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "email")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("name", "email", "password")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    # Customize the admin list view
    list_per_page = 25
    ordering = ("-created_at",)
