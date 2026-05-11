from django.contrib import messages
from django.shortcuts import redirect, render

from .models import BudgetRequest


def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def services(request):
    return render(request, "core/services.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        phone = request.POST.get("phone", "").strip()
        if name and email and message:
            BudgetRequest.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message,
            )
        messages.success(request, "Recebemos sua mensagem e retornaremos em breve.")
        return redirect("core:contact")
    return render(request, "core/contact.html")
