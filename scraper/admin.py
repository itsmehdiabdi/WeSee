import json

from django.contrib import admin
from django.utils.html import format_html

from .models import Scraper, ScrapingTask


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


@admin.register(ScrapingTask)
class ScrapingTaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_id",
        "linkedin_url",
        "status",
        "created_at",
        "updated_at",
        "has_result",
        "has_error",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("task_id", "linkedin_url")
    readonly_fields = (
        "task_id",
        "created_at",
        "updated_at",
        "formatted_result",
        "formatted_error",
    )

    fieldsets = (
        ("Task Information", {"fields": ("task_id", "linkedin_url", "status")}),
        ("Results", {"fields": ("formatted_result",), "classes": ("collapse",)}),
        (
            "Error Details",
            {"fields": ("error_message", "formatted_error"), "classes": ("collapse",)},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    # Customize the admin list view
    list_per_page = 25
    ordering = ("-created_at",)

    def has_result(self, obj):
        """Display if task has results"""
        return bool(obj.result)

    has_result.boolean = True
    has_result.short_description = "Has Result"

    def has_error(self, obj):
        """Display if task has error"""
        return bool(obj.error_message)

    has_error.boolean = True
    has_error.short_description = "Has Error"

    def formatted_result(self, obj):
        """Display formatted JSON result"""
        if obj.result:
            try:
                formatted_json = json.dumps(obj.result, indent=2, ensure_ascii=False)
                return format_html(
                    '<pre style="white-space: pre-wrap; max-height: 400px; overflow-y: auto; '
                    "background: #f8f9fa; padding: 10px; border: 1px solid #dee2e6; "
                    'border-radius: 4px;">{}</pre>',
                    formatted_json,
                )
            except (TypeError, ValueError):
                return format_html(
                    '<pre style="color: red;">Invalid JSON data: {}</pre>',
                    str(obj.result),
                )
        return "No result data"

    formatted_result.short_description = "Formatted Result (JSON)"

    def formatted_error(self, obj):
        """Display formatted error message"""
        if obj.error_message:
            return format_html(
                '<pre style="white-space: pre-wrap; max-height: 200px; overflow-y: auto; '
                "background: #fff3cd; padding: 10px; border: 1px solid #ffeaa7; "
                'border-radius: 4px; color: #856404;">{}</pre>',
                obj.error_message,
            )
        return "No error message"

    formatted_error.short_description = "Formatted Error Message"
