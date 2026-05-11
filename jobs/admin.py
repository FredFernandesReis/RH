from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "department",
        "location",
        "work_model_display",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "work_model")
    search_fields = ("title", "department", "location")
    list_per_page = 50
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    @admin.display(description="Modelo de trabalho", ordering="work_model")
    def work_model_display(self, obj):
        return obj.get_work_model_display()
