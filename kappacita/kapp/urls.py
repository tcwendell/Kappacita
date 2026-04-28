from django.urls import path # type: ignore
from .views import *

urlpatterns = [
    path('', homepage, name = 'homepage'),
<<<<<<< HEAD
    path('cursos/', cursos, name = 'cursos'),
    path('kappabot/', kappabot, name = 'kappabot'),
    path('questionario/', questionario, name = 'questionario'),
    path('profissoes/', profissoes, name = 'profissoes'),
    path('favoritos/', favoritos, name = 'favoritos'),
    path('meuprogresso/', meuprogresso, name = 'meuprogresso'),
    path('artigos/', artigos, name = 'artigos'),
    
]
=======
]
>>>>>>> db5fe9a (alteração irrelevante)
