from django.contrib.auth.models import Group

PANEL_GROUP_NAME = "Equipe Painel Vertice RH"


def user_can_access_panel(user) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    return Group.objects.filter(name=PANEL_GROUP_NAME, user=user).exists()
