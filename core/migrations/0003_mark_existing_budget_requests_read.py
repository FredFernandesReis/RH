from django.db import migrations


def mark_existing_as_read(apps, schema_editor):
    BudgetRequest = apps.get_model("core", "BudgetRequest")
    for br in BudgetRequest.objects.filter(read_at__isnull=True).iterator():
        br.read_at = br.created_at
        br.save(update_fields=["read_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_budgetrequest_phone_read_at"),
    ]

    operations = [
        migrations.RunPython(mark_existing_as_read, migrations.RunPython.noop),
    ]
