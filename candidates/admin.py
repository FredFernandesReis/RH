from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "status", "applied_at")
    list_filter = ("status", "job")
    search_fields = ("full_name", "email", "phone")
