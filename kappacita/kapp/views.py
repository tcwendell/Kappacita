from django.shortcuts import render


def homepage(request):
    return render(request, 'html/homepage.html')

def cursos(request):
    return render(request, 'html/cursos.html')

def login(request):
    return render(request, 'html/login.html')

def kappabot(request):
    return render(request, 'html/kappabot.html')
