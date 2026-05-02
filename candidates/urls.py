from django.urls import path

from .views import apply_to_job

app_name = "candidates"

urlpatterns = [
    path("vaga/<int:job_id>/", apply_to_job, name="apply"),
]
