from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added, social_account_updated, pre_social_login
from .models import Perfil
import requests
from django.core.files.base import ContentFile


def salvar_foto_google(sociallogin, **kwargs):
    user = sociallogin.user
    if not user.pk:
        return

    perfil, _ = Perfil.objects.get_or_create(usuario=user)

    if not perfil.foto:
        foto_url = sociallogin.account.extra_data.get('picture')
        if foto_url:
            try:
                response = requests.get(foto_url, timeout=5)
                if response.status_code == 200:
                    perfil.foto.save(f"google_{user.pk}.jpg", ContentFile(response.content), save=True)
            except Exception:
                pass


social_account_added.connect(salvar_foto_google)
social_account_updated.connect(salvar_foto_google)
pre_social_login.connect(salvar_foto_google)