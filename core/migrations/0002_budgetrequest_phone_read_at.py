from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="budgetrequest",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Solicitação de orçamento",
                "verbose_name_plural": "Solicitações de orçamento",
            },
        ),
        migrations.AddField(
            model_name="budgetrequest",
            name="phone",
            field=models.CharField(blank=True, max_length=40, verbose_name="Telefone"),
        ),
        migrations.AddField(
            model_name="budgetrequest",
            name="read_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Lido em"),
        ),
    ]
