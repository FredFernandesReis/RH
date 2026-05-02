from django.urls import path

from .views import about, contact, home, services

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("sobre/", about, name="about"),
    path("servicos/", services, name="services"),
    path("contato/", contact, name="contact"),
]
