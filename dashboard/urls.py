from django.urls import path

from .views import (
    budget_request_detail,
    delete_application,
    delete_job,
    edit_job,
    panel,
    update_status,
)

app_name = "dashboard"

urlpatterns = [
    path("", panel, name="panel"),
    path("candidatura/<int:application_id>/status/", update_status, name="update_status"),
    path("candidatura/<int:application_id>/excluir/", delete_application, name="delete_application"),
    path("vaga/<int:job_id>/editar/", edit_job, name="edit_job"),
    path("vaga/<int:job_id>/excluir/", delete_job, name="delete_job"),
    path("orcamento/<int:pk>/", budget_request_detail, name="budget_detail"),
]
