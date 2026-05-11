from django.contrib import admin

from .models import BudgetRequest


@admin.register(BudgetRequest)
class BudgetRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "read_at", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at", "read_at")
