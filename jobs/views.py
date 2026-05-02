from django.shortcuts import get_object_or_404, render

from .models import Job


def job_list(request):
    search = request.GET.get("q", "").strip()
    jobs = Job.objects.filter(is_active=True)

    if search:
        jobs = jobs.filter(title__icontains=search)

    context = {
        "jobs": jobs,
        "search": search,
        "total_jobs": jobs.count(),
    }
    return render(request, "jobs/job_list.html", context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    return render(request, "jobs/job_detail.html", {"job": job})
