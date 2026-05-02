from django.urls import path

from .views import job_detail, job_list

app_name = "jobs"

urlpatterns = [
    path("", job_list, name="list"),
    path("<int:pk>/", job_detail, name="detail"),
]
