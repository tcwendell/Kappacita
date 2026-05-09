# kapp/context_processors.py

from .models import Perfil

def perfil_usuario(request):
    """
    Injeta o perfil do usuário logado em todos os templates.
    Retorna None se o usuário não estiver logado ou não tiver perfil.
    """
    if request.user.is_authenticated:
        perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
        return {'perfil_global': perfil}
    return {'perfil_global': None}