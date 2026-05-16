from urllib.parse import urlencode

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from candidates.models import Application
from core.models import BudgetRequest
from jobs.forms import JobForm
from jobs.models import Job

from .decorators import panel_login_required


@panel_login_required
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
            return redirect(reverse("dashboard:panel") + "?" + urlencode({"section": "vagas"}))
    else:
        job_form = JobForm()

    stats = {
        "total": all_applications.count(),
        "new": all_applications.filter(status=Application.Status.NEW).count(),
        "screening": all_applications.filter(status=Application.Status.SCREENING).count(),
        "interview": all_applications.filter(status=Application.Status.INTERVIEW).count(),
        "approved": all_applications.filter(status=Application.Status.APPROVED).count(),
        "rejected": all_applications.filter(status=Application.Status.REJECTED).count(),
    }

    latest_budget = BudgetRequest.objects.order_by("-created_at").first()

    context = {
        "applications": applications,
        "status_filter": status_filter,
        "section": section,
        "statuses": Application.Status.choices,
        "stats": stats,
        "budget_requests": BudgetRequest.objects.all()[:50],
        "budget_unread_count": BudgetRequest.objects.filter(read_at__isnull=True).count(),
        "budget_total_count": BudgetRequest.objects.count(),
        "budget_latest_id": latest_budget.pk if latest_budget else 0,
        "jobs": Job.objects.all(),
        "job_form": job_form,
    }
    return render(request, "dashboard/panel.html", context)


def _budget_requests_payload():
    budget_requests = list(BudgetRequest.objects.all()[:50])
    unread_count = BudgetRequest.objects.filter(read_at__isnull=True).count()
    latest = budget_requests[0] if budget_requests else None
    return {
        "budget_requests": budget_requests,
        "unread_count": unread_count,
        "total_count": BudgetRequest.objects.count(),
        "latest_id": latest.pk if latest else 0,
        "rows_html": render_to_string(
            "dashboard/partials/budget_requests_rows.html",
            {"budget_requests": budget_requests},
        ),
    }


@panel_login_required
def update_status(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    new_status = request.POST.get("status")

    valid_statuses = {value for value, _ in Application.Status.choices}
    if new_status in valid_statuses:
        application.status = new_status
        application.save(update_fields=["status", "updated_at"])
        messages.success(request, "Status atualizado com sucesso.")

    return redirect("dashboard:panel")


@panel_login_required
@require_POST
def delete_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    name = application.full_name
    if application.resume:
        application.resume.delete(save=False)
    application.delete()
    messages.success(request, f"Candidatura de {name} foi excluída.")
    params = {"section": "candidaturas"}
    status_q = request.POST.get("status_filter", "").strip()
    if status_q:
        params["status"] = status_q
    return redirect(reverse("dashboard:panel") + "?" + urlencode(params))


@panel_login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaga atualizada com sucesso.")
            return redirect(reverse("dashboard:panel") + "?" + urlencode({"section": "vagas"}))
    else:
        form = JobForm(instance=job)

    return render(request, "dashboard/job_form.html", {"form": form, "job": job})


@panel_login_required
@require_POST
def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    title = job.title
    applications = list(job.applications.all())
    n_apps = len(applications)
    for app in applications:
        if app.resume:
            app.resume.delete(save=False)
    job.delete()
    if n_apps:
        messages.success(
            request,
            f'Vaga "{title}" excluída. Foram removidas também {n_apps} candidatura(s) vinculadas.',
        )
    else:
        messages.success(request, f'Vaga "{title}" excluída.')
    return redirect(reverse("dashboard:panel") + "?" + urlencode({"section": "vagas"}))


@panel_login_required
def budget_request_detail(request, pk):
    budget_req = get_object_or_404(BudgetRequest, pk=pk)
    if budget_req.read_at is None:
        budget_req.read_at = timezone.now()
        budget_req.save(update_fields=["read_at"])
    return render(
        request,
        "dashboard/budget_detail.html",
        {
            "budget_req": budget_req,
        },
    )


@panel_login_required
@require_POST
def delete_budget_request(request, pk):
    budget_req = get_object_or_404(BudgetRequest, pk=pk)
    name = budget_req.name
    budget_req.delete()
    messages.success(request, f'Solicitação de orçamento de "{name}" foi excluída.')
    next_url = request.POST.get("next") or reverse("dashboard:panel") + "?" + urlencode({"section": "contatos"})
    return redirect(next_url)


@panel_login_required
@require_GET
def budget_requests_refresh(request):
    payload = _budget_requests_payload()
    return JsonResponse(payload)
