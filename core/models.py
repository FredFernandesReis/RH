from django.db import models


class BudgetRequest(models.Model):
    name = models.CharField("Nome", max_length=120)
    email = models.EmailField("E-mail")
    phone = models.CharField("Telefone", max_length=40, blank=True)
    message = models.TextField("Mensagem")
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    read_at = models.DateTimeField("Lido em", null=True, blank=True)

    class Meta:
        verbose_name = "Solicitação de orçamento"
        verbose_name_plural = "Solicitações de orçamento"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"

    @property
    def phone_digits(self) -> str:
        return "".join(c for c in (self.phone or "") if c.isdigit())

    @property
    def whatsapp_url(self) -> str:
        d = self.phone_digits
        if len(d) < 10:
            return ""
        if d.startswith("55"):
            return f"https://wa.me/{d}"
        return f"https://wa.me/55{d}"

    @property
    def is_unread(self) -> bool:
        return self.read_at is None
