from django.db import models


class BudgetRequest(models.Model):
    name = models.CharField("Nome", max_length=120)
    email = models.EmailField("E-mail")
    message = models.TextField("Mensagem")
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Solicitacao de orcamento"
        verbose_name_plural = "Solicitacoes de orcamento"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"
