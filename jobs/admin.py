from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "location", "work_model", "is_active", "created_at")
    list_filter = ("is_active", "work_model", "department")
    search_fields = ("title", "department", "location")
