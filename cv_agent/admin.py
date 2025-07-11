import json

from django.contrib import admin
from django.utils.html import format_html

from .models import CVTask


@admin.register(CVTask)
class CVTaskAdmin(admin.ModelAdmin):
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
        ("Task Information", {"fields": ("task_id", "linkedin_url", "job_description", "status")}),
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
        """Display formatted CV result"""
        if obj.result:
            try:
                # Try to parse as JSON first
                parsed_result = json.loads(obj.result) if isinstance(obj.result, str) else obj.result
                formatted_json = json.dumps(parsed_result, indent=2, ensure_ascii=False)
                return format_html(
                    '<pre style="white-space: pre-wrap; max-height: 400px; overflow-y: auto; '
                    "background: #f8f9fa; padding: 10px; border: 1px solid #dee2e6; "
                    'border-radius: 4px;">{}</pre>',
                    formatted_json,
                )
            except (TypeError, ValueError, json.JSONDecodeError):
                # If not JSON, display as plain text
                return format_html(
                    '<pre style="white-space: pre-wrap; max-height: 400px; overflow-y: auto; '
                    "background: #f8f9fa; padding: 10px; border: 1px solid #dee2e6; "
                    'border-radius: 4px;">{}</pre>',
                    str(obj.result),
                )
        return "No result data"

    formatted_result.short_description = "Formatted Result (CV)"

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
