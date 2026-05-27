from django.core.management.base import BaseCommand
from kapp.models import Curso, Profissao, AreaAtuacao
import cloudinary.uploader
import os

class Command(BaseCommand):
    help = 'Re-cadastra imagens locais no Cloudinary'

    def handle(self, *args, **kwargs):
        self.migrar(Curso.objects.all(),        'icone')
        self.migrar(Profissao.objects.all(),    'icone')
        self.migrar(AreaAtuacao.objects.all(),  'imagem')
        self.stdout.write("Concluído!")

    def migrar(self, queryset, campo_nome):
        from django.conf import settings
        for obj in queryset:
            campo = getattr(obj, campo_nome)
            if not campo:
                continue
            nome = str(campo.name)
            if nome.startswith('http'):
                self.stdout.write(f"[OK] {obj} já no Cloudinary")
                continue
            caminho = os.path.join(settings.MEDIA_ROOT, nome)
            if os.path.exists(caminho):
                resultado = cloudinary.uploader.upload(
                    caminho, folder=os.path.dirname(nome)
                )
                setattr(obj, campo_nome, resultado['public_id'])
                obj.save()
                self.stdout.write(f"[UPLOAD] {obj}")
            else:
                self.stdout.write(f"[SEM ARQUIVO] {obj} — re-cadastre pelo admin")