from django.urls import path # type: ignore
from .views import *

urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('cursos/', cursos, name = 'cursos'),
    path('kappabot/', kappabot, name = 'kappabot'),
    path('questionario/', questionario, name = 'questionario'),
    path('profissoes/', profissoes, name = 'profissoes'),
    path('favoritos/', favoritos, name = 'favoritos'),
    path('meuprogresso/', meuprogresso, name = 'meuprogresso'),
    path('artigos/', artigos, name = 'artigos'),
    path('configuracoes/', configuracoes, name = 'configuracoes'),
    path('questionario/2/', questionario2, name='questionario2'),
    path('questionario/3/', questionario3, name='questionario3'),
    path('questionario/4/', questionario4, name='questionario4'),
    path('questionario/5/', questionario5, name='questionario5'),
]
