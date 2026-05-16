# signals.py
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added, social_account_updated
from .models import Perfil
import requests
from django.core.files.base import ContentFile

def salvar_foto_google(sociallogin, **kwargs):
    user = sociallogin.user
    perfil, _ = Perfil.objects.get_or_create(usuario=user)

    # Só busca se ainda não tiver foto
    if not perfil.foto:
        extra_data = sociallogin.account.extra_data
        foto_url = extra_data.get('picture')

        if foto_url:
            try:
                response = requests.get(foto_url)
                if response.status_code == 200:
                    nome_arquivo = f"google_{user.pk}.jpg"
                    perfil.foto.save(nome_arquivo, ContentFile(response.content), save=True)
            except Exception:
                pass  # Se falhar, fica sem foto mesmo

social_account_added.connect(salvar_foto_google)
social_account_updated.connect(salvar_foto_google)