from django.contrib import admin
from django.urls import path, include
from .views import (
    loginFuncionalidades, loginArea, cadastrarFuncionalidades,
    cadastrarArea, sair, homepage, favoritar_curso_ajax,
    cursos, favoritar_curso, kappabot, questionario,
    questionario2, questionario3, questionario4, questionario5,
    profissoes, favoritar_profissao, favoritos,
    desfavoritar_curso, desfavoritar_profissao, meuprogresso,
    configuracoes, privacidade, notificacoes, idiomas, excluir_conta,
    kappabot_chat, kappabot_nova_sessao
)

urlpatterns = [
    path('', loginFuncionalidades, name='inicio'),
    path('loginFuncionalidades/', loginFuncionalidades, name='loginFuncionalidades'),
    path('loginArea/', loginArea, name='loginArea'),
    path('cadastrarFuncionalidades/', cadastrarFuncionalidades, name='cadastrarFuncionalidades'),
    path('cadastrarArea/', cadastrarArea, name='cadastrarArea'),
    path('sair/', sair, name='sair'),
    path('homepage/', homepage, name='homepage'),
    path('favoritar-ajax/<int:curso_id>/', favoritar_curso_ajax, name='favoritar_curso_ajax'),
    path('cursos/', cursos, name='cursos'),
    path('cursos/<int:curso_id>/favoritar/', favoritar_curso, name='favoritar_curso'),
    path('kappabot/', kappabot, name='kappabot'),
    path('questionario/', questionario, name='questionario'),
    path('questionario/2/', questionario2, name='questionario2'),
    path('questionario/3/', questionario3, name='questionario3'),
    path('questionario/4/', questionario4, name='questionario4'),
    path('questionario/5/', questionario5, name='questionario5'),
    path('profissoes/', profissoes, name='profissoes'),
    path('profissoes/favoritar/<int:profissao_id>/', favoritar_profissao, name='favoritar_profissao'),
    path('favoritos/', favoritos, name='favoritos'),
    path('favoritos/remover-curso/<int:curso_id>/', desfavoritar_curso, name='desfavoritar_curso'),
    path('favoritos/remover-profissao/<int:profissao_id>/', desfavoritar_profissao, name='desfavoritar_profissao'),
    path('meuprogresso/', meuprogresso, name='meuprogresso'),
    path('configuracoes/', configuracoes, name='configuracoes'),
    path('privacidade/', privacidade, name='privacidade'),
    path('notificacoes/', notificacoes, name='notificacoes'),
    path('idiomas/', idiomas, name='idiomas'),
    path('excluir-conta/', excluir_conta, name='excluir_conta'),
    path('kappabot/chat/', kappabot_chat, name='kappabot_chat'),
    path('kappabot/nova-sessao/', kappabot_nova_sessao, name='kappabot_nova_sessao'),
    
]