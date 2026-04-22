from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('cursos/', cursos, name = 'cursos'),
    path('login/', login, name = 'login'),
    path('kappabot/', kappabot, name = 'kappabot'),
    
]