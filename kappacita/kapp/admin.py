from django.contrib import admin
from .models import AreaAtuacao, Profissao, Curso, Favorito


@admin.register(AreaAtuacao)
class AreaAtuacaoAdmin(admin.ModelAdmin):
    list_display  = ('nome',)
    search_fields = ('nome',)
    ordering      = ('nome',)


@admin.register(Profissao)
class ProfissaoAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'area', 'salario_min', 'salario_max', 'avaliacao')
    list_filter   = ('area',)
    search_fields = ('nome',)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'area', 'avaliacao')
    list_filter   = ('area',)
    search_fields = ('nome',)


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'profissao')