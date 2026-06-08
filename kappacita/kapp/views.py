from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.conf import settings
import requests
import json
import os

from .models import (
    AreaAtuacao, Curso, Profissao, Favorito, Perfil,
    RespostaQuestionario, SessaoChat, MensagemChat, LimiteUsoBot,
)

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
    q       = request.GET.get('q', '').strip()
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
        'cursos':        cursos_paginados,
        'areas':         AreaAtuacao.objects.all(),
        'favoritos_ids': favoritos_ids,
        'area_ativa':    int(area_id) if area_id.isdigit() else None,
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
        'favoritos_cursos':     favoritos_cursos,
        'favoritos_profissoes': favoritos_profissoes,
        'filtro':               request.GET.get('filtro', 'todos'),
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
        'resposta':    resposta,
        'selecionados': resposta.get_habilidades(),
    })


@login_required
def questionario3(request):
    resposta, _ = RespostaQuestionario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        resposta.valores_carreira = ','.join(request.POST.getlist('valores_carreira')[:3])
        resposta.save()
        return redirect('questionario4')
    return render(request, 'questionario3.html', {
        'resposta':    resposta,
        'selecionados': resposta.get_valores(),
    })


@login_required
def questionario4(request):
    resposta, _ = RespostaQuestionario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        resposta.estilo_trabalho = request.POST.get('estilo_trabalho', '')
        resposta.save()
        return redirect('questionario5')
    return render(request, 'questionario4.html', {
        'resposta':   resposta,
        'selecionado': resposta.estilo_trabalho,
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
        'resposta':   resposta,
        'selecionado': resposta.escolaridade,
    })


# ── KAPPABOT ──────────────────────────────────────────────────────────────────

def _montar_system_prompt(usuario, resposta):
    """
    Monta o system prompt enviado ao Gemini com o perfil do usuário
    e o catálogo de cursos/profissões da plataforma.
    """
    cursos     = Curso.objects.select_related('area').all()[:50]
    profissoes = Profissao.objects.select_related('area').all()[:50]

    lista_cursos = "\n".join(
        f"- {c.nome} (Área: {c.area.nome if c.area else 'Geral'}, Avaliação: {c.avaliacao})"
        for c in cursos
    ) or "Nenhum curso cadastrado ainda."

    lista_profissoes = "\n".join(
        f"- {p.nome} (Área: {p.area.nome if p.area else 'Geral'}, "
        f"Salário: R${p.salario_min}–R${p.salario_max}, Avaliação: {p.avaliacao})"
        for p in profissoes
    ) or "Nenhuma profissão cadastrada ainda."

    if resposta:
        interesses   = resposta.interesses.replace(',', ', ')      if resposta.interesses      else 'Não informado'
        habilidades  = resposta.habilidades.replace(',', ', ')     if resposta.habilidades     else 'Não informado'
        valores      = resposta.valores_carreira.replace(',', ', ') if resposta.valores_carreira else 'Não informado'
        estilo       = resposta.estilo_trabalho                    if resposta.estilo_trabalho  else 'Não informado'
        escolaridade = resposta.escolaridade                       if resposta.escolaridade     else 'Não informado'
    else:
        interesses = habilidades = valores = estilo = escolaridade = 'Não informado'

    return f"""Você é o KappaBot, assistente de orientação vocacional da plataforma Kappacita.
Seu objetivo é ajudar o usuário a descobrir a melhor área de atuação, curso e profissão com base no perfil dele.

PERFIL DO USUÁRIO ({usuario.username}):
- Interesses: {interesses}
- Habilidades: {habilidades}
- Valores de carreira: {valores}
- Estilo de trabalho preferido: {estilo}
- Escolaridade pretendida: {escolaridade}

CURSOS DISPONÍVEIS NA PLATAFORMA:
{lista_cursos}

PROFISSÕES DISPONÍVEIS NA PLATAFORMA:
{lista_profissoes}

REGRAS IMPORTANTES:
1. Na PRIMEIRA mensagem da conversa (quando não há histórico anterior), apresente AUTOMATICAMENTE uma recomendação clara de área de atuação, curso e profissão baseada no perfil acima. Seja específico e justifique brevemente cada recomendação.
2. Após a recomendação inicial, convide o usuário a fazer perguntas sobre as áreas/cursos/profissões recomendados (ex: salário, mercado de trabalho, como ingressar etc.).
3. Responda SEMPRE em português brasileiro.
4. Seja amigável, encorajador e objetivo.
5. Quando citar profissões ou cursos, use APENAS os que estão listados acima.
6. Mantenha respostas com no máximo 4 parágrafos curtos.
7. Nunca saia do tema de orientação vocacional e carreira.
8. Se o usuário perguntar sobre salário de uma profissão listada, informe o intervalo salarial disponível nos dados acima."""


def _chamar_gemini(api_key, system_prompt, historico_msgs, mensagem_atual):

    modelo = 'gemini-2.5-flash'
    url    = (
        f'https://generativelanguage.googleapis.com/v1beta/models/'
        f'{modelo}:generateContent?key={api_key}'
    )

    # Monta o array contents: histórico + mensagem atual
    contents = []
    for msg in historico_msgs:
        role = 'user' if msg.role == 'user' else 'model'
        contents.append({'role': role, 'parts': [{'text': msg.conteudo}]})
    contents.append({'role': 'user', 'parts': [{'text': mensagem_atual}]})

    payload = {
        'system_instruction': {
            'parts': [{'text': system_prompt}]
        },
        'contents': contents,
        'generationConfig': {
            'maxOutputTokens': 1024,
            'temperature':     0.7,
        },
    }

    response = requests.post(url, json=payload, timeout=30)

    # Captura erros HTTP com mensagem legível
    if not response.ok:
        try:
            detalhe = response.json().get('error', {}).get('message', response.text)
        except Exception:
            detalhe = response.text
        raise ValueError(f'Gemini retornou status {response.status_code}: {detalhe}')

    return response.json()['candidates'][0]['content']['parts'][0]['text']


@login_required
def kappabot(request):
    """Renderiza a página do KappaBot com o histórico da sessão atual."""
    sessao = SessaoChat.objects.filter(
        usuario=request.user
    ).order_by('-criado_em').first()

    mensagens = []
    if sessao:
        mensagens = list(
            sessao.mensagens.order_by('criado_em').values('role', 'conteudo')
        )

    try:
        resposta               = RespostaQuestionario.objects.get(usuario=request.user)
        questionario_concluido = resposta.concluido
    except RespostaQuestionario.DoesNotExist:
        resposta               = None
        questionario_concluido = False

    # Verifica mensagens restantes para exibir no template
    limite, _ = LimiteUsoBot.objects.get_or_create(usuario=request.user)

    return render(request, 'kappabot.html', {
        'mensagens':              mensagens,
        'questionario_concluido': questionario_concluido,
        'mensagens_restantes':    LimiteUsoBot.LIMITE_DIARIO - limite.mensagens_hoje,
    })


@login_required
@require_POST
def kappabot_chat(request):
    # ── 1. Parse do body ──────────────────────────────────────────────────
    try:
        data          = json.loads(request.body)
        mensagem_user = data.get('mensagem', '').strip()
        nova_sessao   = data.get('nova_sessao', False)
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'erro': 'Requisição inválida.'}, status=400)

    if not mensagem_user:
        return JsonResponse({'erro': 'Mensagem vazia.'}, status=400)

    # ── 2. Verifica API Key ANTES de qualquer coisa ───────────────────────
    # Configure a variável de ambiente GEMINI_API_KEY no seu .env ou sistema.
    # Exemplo no .env:  GEMINI_API_KEY=AIzaSy...
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not api_key:
        return JsonResponse(
            {'erro': 'Chave da API do Gemini não configurada. '
                    'Defina a variável de ambiente GEMINI_API_KEY.'},
            status=500
        )

    # ── 3. Verifica limite diário ─────────────────────────────────────────
    limite, _ = LimiteUsoBot.objects.get_or_create(usuario=request.user)
    if not limite.pode_enviar():
        return JsonResponse(
            {'erro': 'Você atingiu o limite de 20 mensagens por dia. Volte amanhã!'},
            status=429
        )

    # ── 4. Busca perfil do usuário ────────────────────────────────────────
    try:
        resposta_quest = RespostaQuestionario.objects.get(usuario=request.user)
    except RespostaQuestionario.DoesNotExist:
        resposta_quest = None

    # ── 5. Busca ou cria sessão de chat ───────────────────────────────────
    if nova_sessao:
        sessao = SessaoChat.objects.create(usuario=request.user, origem='direto')
    else:
        sessao = (
            SessaoChat.objects.filter(usuario=request.user)
            .order_by('-criado_em')
            .first()
        )
        if not sessao:
            sessao = SessaoChat.objects.create(usuario=request.user, origem='direto')

    is_primeira_mensagem = not sessao.mensagens.exists()

    # Salva mensagem do usuário
    MensagemChat.objects.create(
        sessao=sessao, role='user', conteudo=mensagem_user
    )

    total_msgs   = sessao.mensagens.count()
    historico_db = list(
        sessao.mensagens.order_by('criado_em')[: total_msgs - 1]
    )
    # Limita às últimas 20 para não estourar o contexto
    historico_db = historico_db[-20:]

    # ── 8. Monta system prompt ────────────────────────────────────────────
    system_prompt = _montar_system_prompt(request.user, resposta_quest)

    # Na primeira mensagem, injeta instrução extra para recomendar imediatamente
    if is_primeira_mensagem:
        system_prompt += (
            "\n\nINSTRUÇÃO ESPECIAL: Esta é a PRIMEIRA mensagem do usuário. "
            "Independentemente do que ele escreveu, comece sua resposta com uma "
            "recomendação personalizada de área de atuação, curso e profissão "
            "baseada no perfil dele. Depois responda normalmente à mensagem dele."
        )

    # ── 9. Chama o Gemini ─────────────────────────────────────────────────
    try:
        resposta_bot = _chamar_gemini(
            api_key       = api_key,
            system_prompt = system_prompt,
            historico_msgs= historico_db,
            mensagem_atual= mensagem_user,
        )
    except requests.exceptions.Timeout:
        return JsonResponse(
            {'erro': 'O KappaBot demorou demais para responder. Tente novamente.'},
            status=504
        )
    except ValueError as e:
        return JsonResponse({'erro': str(e)}, status=500)
    except Exception as e:
        return JsonResponse(
            {'erro': f'Erro inesperado ao contatar o KappaBot: {str(e)}'},
            status=500
        )

    # ── 10. Salva resposta e registra uso ─────────────────────────────────
    MensagemChat.objects.create(
        sessao=sessao, role='assistant', conteudo=resposta_bot
    )
    limite.registrar_envio()

    return JsonResponse({
        'resposta':            resposta_bot,
        'sessao_id':           sessao.id,
        'mensagens_restantes': LimiteUsoBot.LIMITE_DIARIO - limite.mensagens_hoje,
        'primeira_mensagem':   is_primeira_mensagem,
    })


@login_required
@require_POST
def kappabot_nova_sessao(request):
    """Cria uma nova sessão de chat, limpando o histórico da tela."""
    sessao = SessaoChat.objects.create(usuario=request.user, origem='direto')
    return JsonResponse({'sessao_id': sessao.id})


# ── OUTRAS PÁGINAS ────────────────────────────────────────────────────────────

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
    return render(request, 'idiomas.html', {
        'idioma_atual': perfil.idioma,
        'prefs':        perfil,
    })


@login_required
def configuracoes(request):
    user      = request.user
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