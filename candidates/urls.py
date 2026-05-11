from django.urls import path

from .views import apply_success, apply_to_job

app_name = "candidates"

urlpatterns = [
    path("vaga/<int:job_id>/", apply_to_job, name="apply"),
    path("vaga/<int:job_id>/enviado/", apply_success, name="apply_success"),
]
