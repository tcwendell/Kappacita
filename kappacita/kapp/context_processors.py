from .models import Perfil

def perfil_usuario(request):
    if request.user.is_authenticated:
        perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
        return {'perfil': perfil}
    return {'perfil': None}