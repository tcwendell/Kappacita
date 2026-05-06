from django.contrib import admin
from .models import Profissao, Curso, Categoria, Favorito

admin.site.register(Profissao)
admin.site.register(Curso)
admin.site.register(Categoria)
admin.site.register(Favorito)
