from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .permissions import user_can_access_panel


def panel_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not user_can_access_panel(request.user):
            messages.error(
                request,
                "Sua conta não tem permissão para acessar o painel. Peça a um administrador para incluir você no grupo "
                '"Equipe Painel Vertice RH" ou marque "Status da equipe" no cadastro do usuário.',
            )
            return redirect("core:home")
        return view_func(request, *args, **kwargs)

    return _wrapped
