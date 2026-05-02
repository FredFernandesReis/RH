from django.db import models
from jobs.models import Job


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = "novo", "Novo"
        SCREENING = "triagem", "Triagem"
        INTERVIEW = "entrevista", "Entrevista"
        APPROVED = "aprovado", "Aprovado"
        REJECTED = "reprovado", "Reprovado"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField("Nome completo", max_length=120)
    email = models.EmailField("E-mail")
    phone = models.CharField("Telefone", max_length=30)
    resume = models.FileField("Curriculo", upload_to="resumes/")
    message = models.TextField("Mensagem", blank=True)
    lgpd_consent = models.BooleanField("Consentimento LGPD", default=False)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    applied_at = models.DateTimeField("Candidatura em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"
