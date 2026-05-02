from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["full_name", "email", "phone", "resume", "message", "lgpd_consent"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "lgpd_consent": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "message": "Resumo profissional (opcional)",
            "lgpd_consent": "Concordo com o uso dos meus dados para processos seletivos.",
        }
