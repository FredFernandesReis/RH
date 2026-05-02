from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from candidates.models import Application
from core.models import BudgetRequest
from jobs.forms import JobForm
from jobs.models import Job


@login_required
def panel(request):
    status_filter = request.GET.get("status", "").strip()
    section = request.GET.get("section", "candidaturas")
    all_applications = Application.objects.select_related("job")
    applications = all_applications
    if status_filter:
        applications = applications.filter(status=status_filter)

    if request.method == "POST" and request.POST.get("action") == "create_job":
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            job_form.save()
            messages.success(request, "Vaga criada com sucesso.")
            return redirect("dashboard:panel")
    else:
        job_form = JobForm()

    stats = {
        "total": all_applications.count(),
        "new": all_applications.filter(status=Application.Status.NEW).count(),
        "screening": all_applications.filter(status=Application.Status.SCREENING).count(),
        "interview": all_applications.filter(status=Application.Status.INTERVIEW).count(),
        "approved": all_applications.filter(status=Application.Status.APPROVED).count(),
    }

    context = {
        "applications": applications,
        "status_filter": status_filter,
        "section": section,
        "statuses": Application.Status.choices,
        "stats": stats,
        "budget_requests": BudgetRequest.objects.all()[:8],
        "jobs": Job.objects.all(),
        "job_form": job_form,
    }
    return render(request, "dashboard/panel.html", context)


@login_required
def update_status(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    new_status = request.POST.get("status")

    valid_statuses = {value for value, _ in Application.Status.choices}
    if new_status in valid_statuses:
        application.status = new_status
        application.save(update_fields=["status", "updated_at"])
        messages.success(request, "Status atualizado com sucesso.")

    return redirect("dashboard:panel")


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaga atualizada com sucesso.")
            return redirect("dashboard:panel")
    else:
        form = JobForm(instance=job)

    return render(request, "dashboard/job_form.html", {"form": form, "job": job})
