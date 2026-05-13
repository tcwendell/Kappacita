from django.contrib import admin
from .models import Profissao, Curso, CategoriaCurso, CategoriaProfissao, Favorito

admin.site.register(Profissao)
admin.site.register(Curso)
admin.site.register(CategoriaCurso)
admin.site.register(CategoriaProfissao)
admin.site.register(Favorito)