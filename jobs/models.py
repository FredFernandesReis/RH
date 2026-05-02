from django.db import models


class Job(models.Model):
    class WorkModel(models.TextChoices):
        PRESENTIAL = "presencial", "Presencial"
        HYBRID = "hibrido", "Hibrido"
        REMOTE = "remoto", "Remoto"

    title = models.CharField("Titulo", max_length=120)
    department = models.CharField("Area", max_length=80)
    location = models.CharField("Localizacao", max_length=120)
    work_model = models.CharField(
        "Modelo de trabalho",
        max_length=20,
        choices=WorkModel.choices,
        default=WorkModel.PRESENTIAL,
    )
    description = models.TextField("Descricao")
    requirements = models.TextField("Requisitos")
    is_active = models.BooleanField("Ativa", default=True)
    created_at = models.DateTimeField("Criada em", auto_now_add=True)

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
