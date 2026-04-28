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
<<<<<<< HEAD
    path('configuracoes/', configuracoes, name = 'configuracoes'),
=======
    
>>>>>>> fd9e39b (testee)
]