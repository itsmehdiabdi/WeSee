from django.contrib import admin

from .models import Accomplishment, Education, Experience, Interest, User


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0
    fields = ("position_title", "institution_name", "from_date", "to_date", "location")
    readonly_fields = ("created_at",)


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0
    fields = ("degree", "institution_name", "from_date", "to_date")
    readonly_fields = ("created_at",)


class InterestInline(admin.TabularInline):
    model = Interest
    extra = 0
    fields = ("name",)
    readonly_fields = ("created_at",)


class AccomplishmentInline(admin.TabularInline):
    model = Accomplishment
    extra = 0
    fields = ("title", "description")
    readonly_fields = ("created_at",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "job_title",
        "company",
        "location",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at", "company")
    search_fields = ("name", "job_title", "company", "linkedin_url")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "job_title", "company", "location", "linkedin_url")},
        ),
        ("About", {"fields": ("about",), "classes": ("collapse",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    inlines = [ExperienceInline, EducationInline, InterestInline, AccomplishmentInline]

    # Customize the admin list view
    list_per_page = 25
    ordering = ("-created_at",)
