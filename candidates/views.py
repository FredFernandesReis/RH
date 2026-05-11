from django.shortcuts import get_object_or_404, redirect, render

from jobs.models import Job

from .forms import ApplicationForm


def apply_to_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, is_active=True)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            return redirect("candidates:apply_success", job_id=job.id)
    else:
        form = ApplicationForm()

    return render(request, "candidates/apply_form.html", {"form": form, "job": job})


def apply_success(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, "candidates/apply_success.html", {"job": job})
