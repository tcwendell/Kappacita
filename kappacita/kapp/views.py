from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator


# ---------- AUTH ----------

def loginFuncionalidades(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'E-mail ou senha incorretos.')

    return render(request, 'loginFuncionalidades.html')


def loginArea(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'E-mail ou senha incorretos.')

    return render(request, 'loginArea.html')


def cadastrarFuncionalidades(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        email_confirm = request.POST.get('email_confirm')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if email != email_confirm:
            messages.error(request, 'Os e-mails não coincidem.')
            return render(request, 'cadastrarFuncionalidades.html')

        if password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastrarFuncionalidades.html')

        if len(password1) < 8:
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres.')
            return render(request, 'cadastrarFuncionalidades.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'cadastrarFuncionalidades.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'cadastrarFuncionalidades.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Conta criada com sucesso! Faça o login.')
        return redirect('loginFuncionalidades')

    return render(request, 'cadastrarFuncionalidades.html')


def cadastrarArea(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        email_confirm = request.POST.get('email_confirm')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if email != email_confirm:
            messages.error(request, 'Os e-mails não coincidem.')
            return render(request, 'cadastrarArea.html')

        if password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastrarArea.html')

        if len(password1) < 8:
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres.')
            return render(request, 'cadastrarArea.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'cadastrarArea.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'cadastrarArea.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Conta criada com sucesso! Faça o login.')
        return redirect('loginFuncionalidades')

    return render(request, 'cadastrarArea.html')


def sair(request):
    logout(request)
    return redirect('loginFuncionalidades')


# ---------- PÁGINAS PROTEGIDAS ----------

@login_required
def homepage(request):
    return render(request, 'homepage.html')

@login_required
def cursos(request):
    return render(request, 'cursos.html')

@login_required
def kappabot(request):
    return render(request, 'kappabot.html')

@login_required
def questionario(request):
    return render(request, 'questionario.html')

@login_required
def questionario2(request):
    return render(request, 'questionario2.html')

@login_required
def questionario3(request):
    return render(request, 'questionario3.html')

@login_required
def questionario4(request):
    return render(request, 'questionario4.html')

@login_required
def questionario5(request):
    return render(request, 'questionario5.html')

@login_required
def profissoes(request):
    q = request.GET.get('q', '')
    lista = Profissao.objects.filter(nome__icontains=q)
    paginator = Paginator(lista, 12)
    page = request.GET.get('page')
    profissoes = paginator.get_page(page)
    return render(request, 'profissoes.html', {'profissoes': profissoes})

@login_required
def favoritos(request):
    return render(request, 'favoritos.html')

@login_required
def meuprogresso(request):
    return render(request, 'meuprogresso.html')

@login_required
def artigos(request):
    return render(request, 'artigos.html')

@login_required
def configuracoes(request):
    return render(request, 'configuracoes.html')

@login_required
def privacidade(request):
    return render(request, 'privacidade.html')

@login_required
def notificacoes(request):
    return render(request, 'notificacoes.html')

@login_required
def idiomas(request):
    return render(request, 'idiomas.html')