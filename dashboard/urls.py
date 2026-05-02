from django.urls import path

from .views import edit_job, panel, update_status

app_name = "dashboard"

urlpatterns = [
    path("", panel, name="panel"),
    path("candidatura/<int:application_id>/status/", update_status, name="update_status"),
    path("vaga/<int:job_id>/editar/", edit_job, name="edit_job"),
]
