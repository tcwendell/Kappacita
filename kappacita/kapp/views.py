from django.shortcuts import render # type: ignore


def homepage(request):
    return render(request, 'homepage.html')

def cursos(request):
    return render(request, 'cursos.html')

def kappabot(request):
    return render(request, 'kappabot.html')

def questionario(request):
    return render(request, 'questionario.html')

def profissoes(request):
    return render(request, 'profissoes.html')

def favoritos(request):
    return render(request, 'favoritos.html')

def meuprogresso(request):
    return render(request, 'meuprogresso.html')

def artigos(request):
    return render(request, 'artigos.html')

def configuracoes(request):
    return render(request, 'configuracoes.html')

def questionario2(request):
    return render(request, 'questionario2.html')

def questionario3(request):
    return render(request, 'questionario3.html')

def questionario4(request):
    return render(request, 'questionario4.html')

def questionario5(request):
    return render(request, 'questionario4.html')


