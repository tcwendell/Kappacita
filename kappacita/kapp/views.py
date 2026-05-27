from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import (
    AreaAtuacao, Curso, Profissao, Favorito, Perfil,
    RespostaQuestionario, SessaoChat, MensagemChat, LimiteUsoBot,
)
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST


# ── AUTH ──────────────────────────────────────────────────────────────────────

def loginFuncionalidades(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        email    = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user     = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('homepage')
        messages.error(request, 'E-mail ou senha incorretos.')

    return render(request, 'loginFuncionalidades.html')


def loginArea(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        email    = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user     = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('homepage')
        messages.error(request, 'E-mail ou senha incorretos.')

    return render(request, 'loginArea.html')


def cadastrarFuncionalidades(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username      = request.POST.get('username')
        email         = request.POST.get('email')
        email_confirm = request.POST.get('email_confirm')
        password1     = request.POST.get('password1')
        password2     = request.POST.get('password2')

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

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, 'Conta criada com sucesso! Faça o login.')
        return redirect('loginFuncionalidades')

    return render(request, 'cadastrarFuncionalidades.html')


def cadastrarArea(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username      = request.POST.get('username')
        email         = request.POST.get('email')
        email_confirm = request.POST.get('email_confirm')
        password1     = request.POST.get('password1')
        password2     = request.POST.get('password2')

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

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, 'Conta criada com sucesso! Faça o login.')
        return redirect('loginFuncionalidades')

    return render(request, 'cadastrarArea.html')

@require_POST
def sair(request):
    logout(request)
    return redirect('loginFuncionalidades')

# ── HOME ──────────────────────────────────────────────────────────────────────

@login_required
def homepage(request):
    cursos_recomendados = Curso.objects.order_by('-avaliacao')[:6]

    favoritos_ids = list(
        Favorito.objects.filter(usuario=request.user)
        .values_list('curso_id', flat=True)
    )

    cursos_salvos = Favorito.objects.filter(
        usuario=request.user, curso__isnull=False
    ).count()

    try:
        resposta = RespostaQuestionario.objects.get(usuario=request.user)
        campos = [
            resposta.interesses,
            resposta.habilidades,
            resposta.valores_carreira,
            resposta.estilo_trabalho,
            resposta.escolaridade,
        ]
        preenchidos = sum(1 for c in campos if c)
        perfil_percentual = int((preenchidos / len(campos)) * 100)
    except RespostaQuestionario.DoesNotExist:
        perfil_percentual = 0

    return render(request, 'homepage.html', {
        'cursos_recomendados': cursos_recomendados,
        'favoritos_ids':       favoritos_ids,
        'cursos_salvos':       cursos_salvos,
        'perfil_percentual':   perfil_percentual,
    })

# ── FAVORITAR CURSO (AJAX toggle) ─────────────────────────────────────────────

@login_required
@require_POST
def favoritar_curso_ajax(request, curso_id):
    try:
        curso = Curso.objects.get(id=curso_id)
    except Curso.DoesNotExist:
        return JsonResponse({'erro': 'Curso não encontrado.'}, status=404)

    favorito, criado = Favorito.objects.get_or_create(usuario=request.user, curso=curso)
    if not criado:
        favorito.delete()

    return JsonResponse({'favoritado': criado, 'curso_id': curso_id})


# ── CURSOS ────────────────────────────────────────────────────────────────────

@login_required
def cursos(request):
    q    = request.GET.get('q', '').strip()
    area_id = request.GET.get('area', '').strip()

    qs = Curso.objects.select_related('area').all()

    if q:
        qs = qs.filter(nome__icontains=q)
    if area_id:
        qs = qs.filter(area_id=area_id)
        
    qs = qs.order_by('nome')

    paginator        = Paginator(qs, 9)
    cursos_paginados = paginator.get_page(request.GET.get('page', 1))

    favoritos_ids = set(
        Favorito.objects.filter(usuario=request.user, curso__isnull=False)
        .values_list('curso_id', flat=True)
    )

    return render(request, 'cursos.html', {
        'cursos':       cursos_paginados,
        'areas':        AreaAtuacao.objects.all(),          
        'favoritos_ids': favoritos_ids,
        'area_ativa':   int(area_id) if area_id.isdigit() else None,
    })


@login_required
@require_POST
def favoritar_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    favorito, criado = Favorito.objects.get_or_create(usuario=request.user, curso=curso)
    if not criado:
        favorito.delete()
    return redirect('cursos')


# ── PROFISSÕES ────────────────────────────────────────────────────────────────

@login_required
def profissoes(request):
    q       = request.GET.get('q', '').strip()
    area_id = request.GET.get('area', '').strip()

    qs = Profissao.objects.select_related('area').all()

    if q:
        qs = qs.filter(nome__icontains=q)
    if area_id:
        qs = qs.filter(area_id=area_id)

    qs = qs.order_by('nome')

    paginator            = Paginator(qs, 9)
    profissoes_paginadas = paginator.get_page(request.GET.get('page', 1))

    favoritos_ids = set(
        Favorito.objects.filter(usuario=request.user, profissao__isnull=False)
        .values_list('profissao_id', flat=True)
    )

    return render(request, 'profissoes.html', {
        'profissoes':    profissoes_paginadas,
        'areas':         AreaAtuacao.objects.all(),
        'favoritos_ids': favoritos_ids,
        'area_ativa':    int(area_id) if area_id.isdigit() else None,
    })


@login_required
@require_POST
def favoritar_profissao(request, profissao_id):
    profissao = Profissao.objects.get(id=profissao_id)
    favorito, criado = Favorito.objects.get_or_create(usuario=request.user, profissao=profissao)
    if not criado:
        favorito.delete()
    return redirect('profissoes')


# ── FAVORITOS ─────────────────────────────────────────────────────────────────

@login_required
def favoritos(request):
    favoritos_cursos = Favorito.objects.filter(
        usuario=request.user, curso__isnull=False
    ).select_related('curso')

    favoritos_profissoes = Favorito.objects.filter(
        usuario=request.user, profissao__isnull=False
    ).select_related('profissao')

    return render(request, 'favoritos.html', {
        'favoritos_cursos':    favoritos_cursos,
        'favoritos_profissoes': favoritos_profissoes,
        'filtro': request.GET.get('filtro', 'todos'),
    })


@login_required
@require_POST
def desfavoritar_curso(request, curso_id):
    Favorito.objects.filter(usuario=request.user, curso_id=curso_id).delete()
    return JsonResponse({'ok': True})


@login_required
@require_POST
def desfavoritar_profissao(request, profissao_id):
    Favorito.objects.filter(usuario=request.user, profissao_id=profissao_id).delete()
    return JsonResponse({'ok': True})


# ── QUESTIONÁRIO ──────────────────────────────────────────────────────────────

@login_required
def questionario(request):
    resposta, _ = RespostaQuestionario.objects.get_or_create(usuario=request.user)
    opcoes_interesses = [
        'Tecnologia', 'Saúde', 'Educação',
        'Negócios e Empreendedorismo', 'Arte e Design', 'Direito e Ciências Sociais',
    ]
    if request.method == 'POST':
        resposta.interesses = ','.join(request.POST.getlist('interesses'))
        resposta.save()
        return redirect('questionario2')

    return render(request, 'questionario.html', {
        'resposta':          resposta,
        'selecionados':      resposta.get_interesses(),
        'opcoes_interesses': opcoes_interesses,
    })


@login_required
def questionario2(request):
    resposta, _ = RespostaQuestionario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        resposta.habilidades = ','.join(request.POST.getlist('habilidades')[:3])
        resposta.save()
        return redirect('questionario3')
    return render(request, 'questionario2.html', {
        'resposta': resposta, 'selecionados': resposta.get_habilidades(),
    })


@login_required
def questionario3(request):
    resposta, _ = RespostaQuestionario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        resposta.valores_carreira = ','.join(request.POST.getlist('valores_carreira')[:3])
        resposta.save()
        return redirect('questionario4')
    return render(request, 'questionario3.html', {
        'resposta': resposta, 'selecionados': resposta.get_valores(),
    })


@login_required
def questionario4(request):
    resposta, _ = RespostaQuestionario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        resposta.estilo_trabalho = request.POST.get('estilo_trabalho', '')
        resposta.save()
        return redirect('questionario5')
    return render(request, 'questionario4.html', {
        'resposta': resposta, 'selecionado': resposta.estilo_trabalho,
    })


@login_required
def questionario5(request):
    resposta, _ = RespostaQuestionario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        resposta.escolaridade = request.POST.get('escolaridade', '')
        resposta.concluido    = True
        resposta.save()
        return redirect('kappabot')
    return render(request, 'questionario5.html', {
        'resposta': resposta, 'selecionado': resposta.escolaridade,
    })


# ── OUTRAS PÁGINAS ────────────────────────────────────────────────────────────

@login_required
def kappabot(request):
    return render(request, 'kappabot.html')

@login_required
def meuprogresso(request):
    return render(request, 'meuprogresso.html')

@login_required
def privacidade(request):
    return render(request, 'privacidade.html')

@login_required
def notificacoes(request):
    return render(request, 'notificacoes.html')

@login_required
def idiomas(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        perfil.idioma            = request.POST.get('idioma', 'pt-br')
        perfil.alto_contraste    = 'alto_contraste' in request.POST
        perfil.tamanho_fonte     = request.POST.get('tamanho_fonte', 'normal')
        perfil.reduzir_animacoes = 'reduzir_animacoes' in request.POST
        perfil.save()
        messages.success(request, 'Preferências salvas com sucesso!')
        return redirect('idiomas')
    return render(request, 'idiomas.html', {'idioma_atual': perfil.idioma, 'prefs': perfil})


@login_required
def configuracoes(request):
    user   = request.user
    perfil, _ = Perfil.objects.get_or_create(usuario=user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'salvar':
            first_name = request.POST.get('first_name', '').strip()
            last_name  = request.POST.get('last_name', '').strip()
            email      = request.POST.get('email', '').strip()

            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, 'Este e-mail já está em uso por outra conta.')
            else:
                user.first_name = first_name
                user.last_name  = last_name
                user.email      = email
                user.save()
                if 'foto' in request.FILES:
                    perfil.foto = request.FILES['foto']
                    perfil.save()
                if request.POST.get('remover_foto') == '1':
                    perfil.foto.delete(save=True)
                messages.success(request, 'Alterações salvas com sucesso!')
            return redirect('configuracoes')

        elif action == 'alterar_senha':
            senha_atual = request.POST.get('senha_atual')
            nova_senha  = request.POST.get('nova_senha')
            confirmar   = request.POST.get('confirmar_senha')

            if not user.check_password(senha_atual):
                messages.error(request, 'Senha atual incorreta.')
            elif nova_senha != confirmar:
                messages.error(request, 'As novas senhas não coincidem.')
            elif len(nova_senha) < 8:
                messages.error(request, 'A nova senha deve ter pelo menos 8 caracteres.')
            else:
                user.set_password(nova_senha)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso!')
            return redirect('configuracoes')

    return render(request, 'configuracoes.html', {'perfil': perfil})


@login_required
@require_POST
def excluir_conta(request):
    senha = request.POST.get('senha_confirmacao')
    user  = request.user
    if not user.check_password(senha):
        messages.error(request, 'Senha incorreta. Sua conta não foi excluída.')
        return redirect('privacidade')
    logout(request)
    user.delete()
    messages.success(request, 'Sua conta foi excluída com sucesso.')
    return redirect('loginFuncionalidades')