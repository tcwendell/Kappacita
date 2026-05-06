from django.urls import path
from .views import *

urlpatterns = [
    # Raiz vai direto pro login
    path('', loginFuncionalidades, name='inicio'),

    # Auth
    path('loginFuncionalidades/', loginFuncionalidades, name='loginFuncionalidades'),
    path('loginArea/', loginArea, name='loginArea'),
    path('cadastrarFuncionalidades/', cadastrarFuncionalidades, name='cadastrarFuncionalidades'),
    path('cadastrarArea/', cadastrarArea, name='cadastrarArea'),
    path('sair/', sair, name='sair'),

    # Páginas protegidas
    path('homepage/', homepage, name='homepage'),
    path('cursos/', cursos, name='cursos'),
    path('kappabot/', kappabot, name='kappabot'),
    path('questionario/', questionario, name='questionario'),
    path('questionario/2/', questionario2, name='questionario2'),
    path('questionario/3/', questionario3, name='questionario3'),
    path('questionario/4/', questionario4, name='questionario4'),
    path('questionario/5/', questionario5, name='questionario5'),
    path('profissoes/', profissoes, name='profissoes'),
    path('favoritos/', favoritos, name='favoritos'),
    path('meuprogresso/', meuprogresso, name='meuprogresso'),
    path('artigos/', artigos, name='artigos'),
    path('configuracoes/', configuracoes, name='configuracoes'),
    path('privacidade/', privacidade, name='privacidade'),
    path('notificacoes/', notificacoes, name='notificacoes'),
    path('idiomas/', idiomas, name='idiomas'),
    path('cursos/<int:curso_id>/favoritar/', favoritar_curso, name='favoritar_curso'),
]