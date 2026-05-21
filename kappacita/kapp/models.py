from django.db import models
from django.contrib.auth.models import User

class CategoriaCurso(models.Model):

    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='categorias_cursos/', blank=True, null=True)

    class Meta:
        verbose_name = 'Categoria de Curso'
        verbose_name_plural = 'Categorias de Cursos'

    def __str__(self):
        return self.nome


class CategoriaProfissao(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='categorias_profissoes/', blank=True, null=True)

    class Meta:
        verbose_name = 'Categoria de Profissão'
        verbose_name_plural = 'Categorias de Profissões'

    def __str__(self):
        return self.nome


class Profissao(models.Model):
    nome = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, default='')
    salario_min = models.DecimalField(max_digits=10, decimal_places=2)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2)
    icone = models.ImageField(blank=True, null=True)
    avaliacao = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)

    categoria = models.ForeignKey(
        CategoriaProfissao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profissoes'
    )

    class Meta:
        verbose_name = 'Profissão'
        verbose_name_plural = 'Profissões'

    def __str__(self):
        return self.nome


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    descricao = models.TextField()
    avaliacao = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    icone = models.ImageField(upload_to='cursos/icones/', blank=True, null=True)

    categoria = models.ForeignKey(
        CategoriaCurso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cursos'
    )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.nome


class Favorito(models.Model):
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE)
    curso     = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    profissao = models.ForeignKey(Profissao, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'curso'],
                condition=models.Q(curso__isnull=False),
                name='unique_favorito_curso'
            ),
            models.UniqueConstraint(
                fields=['usuario', 'profissao'],
                condition=models.Q(profissao__isnull=False),
                name='unique_favorito_profissao'
            ),
        ]

    def __str__(self):
        if self.curso:
            return f'{self.usuario.username} → {self.curso.nome}'
        if self.profissao:
            return f'{self.usuario.username} → {self.profissao.nome}'
        return f'{self.usuario.username} → (sem vínculo)'


class Perfil(models.Model):
    IDIOMA_CHOICES = [
        ('pt-br', 'Português (Brasil)'),
        ('en',    'English'),
        ('es',    'Español'),
    ]
    FONTE_CHOICES = [
        ('normal',       'Normal'),
        ('grande',       'Grande'),
        ('muito_grande', 'Muito grande'),
    ]

    usuario           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto              = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    idioma            = models.CharField(max_length=10, choices=IDIOMA_CHOICES, default='pt-br')
    alto_contraste    = models.BooleanField(default=False)
    tamanho_fonte     = models.CharField(max_length=20, choices=FONTE_CHOICES, default='normal')
    reduzir_animacoes = models.BooleanField(default=False)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
    
# ── QUESTIONÁRIO VOCACIONAL 
class RespostaQuestionario(models.Model):
    interesses = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Áreas de interesse'
    )

    # ── Etapa 2: Habilidades (múltipla escolha, até 3)
    HABILIDADES_CHOICES = [
        ('comunicacao',    'Comunicação e oratória'),
        ('logica',         'Raciocínio lógico e analítico'),
        ('criatividade',   'Criatividade e inovação'),
        ('organizacao',    'Organização e planejamento'),
        ('empatia',        'Empatia e relações interpessoais'),
        ('pesquisa',       'Pesquisa e análise de dados'),
    ]
    habilidades = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Habilidades selecionadas'
    )

    # ── Etapa 3: Valores de carreira (múltipla escolha, até 3)
    VALORES_CHOICES = [
        ('salario',        'Alto salário e estabilidade financeira'),
        ('impacto',        'Impacto social e ajudar pessoas'),
        ('expressao',      'Criatividade e expressão pessoal'),
        ('aprendizado',    'Crescimento intelectual e aprendizado'),
        ('flexibilidade',  'Flexibilidade e qualidade de vida'),
        ('prestigio',      'Reconhecimento e prestígio profissional'),
    ]
    valores_carreira = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Valores de carreira'
    )

    # ── Etapa 4: Estilo de trabalho (escolha única)
    ESTILO_CHOICES = [
        ('solo',        'Sozinho, com foco e autonomia'),
        ('equipe',      'Em equipe, colaborando com outros'),
        ('publico',     'Com o público, atendendo pessoas'),
        ('campo',       'Em campo, com atividades práticas'),
    ]
    estilo_trabalho = models.CharField(
        max_length=20,
        choices=ESTILO_CHOICES,
        blank=True,
        verbose_name='Estilo de trabalho'
    )

    # ── Etapa 5: Escolaridade pretendida (escolha única)
    ESCOLARIDADE_CHOICES = [
        ('tecnico',     'Curso técnico'),
        ('graduacao',   'Graduação'),
        ('pos',         'Pós-Graduação / Especialização'),
        ('mestrado',    'Mestrado ou Doutorado'),
    ]
    escolaridade = models.CharField(
        max_length=20,
        choices=ESCOLARIDADE_CHOICES,
        blank=True,
        verbose_name='Escolaridade pretendida'
    )

# ── Metadados 
    usuario      = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='resposta_questionario'
    )
    concluido    = models.BooleanField(default=False)
    criado_em    = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Resposta do Questionário'
        verbose_name_plural = 'Respostas do Questionário'

    def __str__(self):
        return f'Questionário de {self.usuario.username} ({"concluído" if self.concluido else "em andamento"})'

    def get_habilidades(self):
        return self.habilidades.split(',') if self.habilidades else []

    def get_valores(self):
        return self.valores_carreira.split(',') if self.valores_carreira else []

    def get_interesses(self):
        return self.interesses.split(',') if self.interesses else []

# ── KAPPABOT: HISTÓRICO E LIMITE DE USO
class SessaoChat(models.Model):
    usuario    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessoes_chat')
    criado_em  = models.DateTimeField(auto_now_add=True)
    # Origem da sessão: veio do questionário ou entrou direto
    origem     = models.CharField(
        max_length=20,
        choices=[('questionario', 'Questionário'), ('direto', 'Direto')],
        default='direto'
    )

    class Meta:
        verbose_name = 'Sessão de Chat'
        ordering = ['-criado_em']

    def __str__(self):
        return f'Sessão de {self.usuario.username} em {self.criado_em:%d/%m/%Y %H:%M}'


class MensagemChat(models.Model):
    ROLE_CHOICES = [('user', 'Usuário'), ('assistant', 'KappaBot')]

    sessao     = models.ForeignKey(SessaoChat, on_delete=models.CASCADE, related_name='mensagens')
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES)
    conteudo   = models.TextField()
    criado_em  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem do Chat'
        ordering = ['criado_em']

    def __str__(self):
        return f'[{self.role}] {self.conteudo[:60]}'


class LimiteUsoBot(models.Model):
    LIMITE_DIARIO = 20

    usuario          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='limite_bot')
    mensagens_hoje   = models.PositiveIntegerField(default=0)
    data_contagem    = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Limite de Uso do Bot'

    def __str__(self):
        return f'{self.usuario.username}: {self.mensagens_hoje}/{self.LIMITE_DIARIO} hoje'

    def resetar_se_novo_dia(self):
        """Zera o contador automaticamente se mudou o dia."""
        from django.utils import timezone
        hoje = timezone.localdate()
        if self.data_contagem < hoje:
            self.mensagens_hoje = 0
            self.data_contagem  = hoje
            self.save()

    def pode_enviar(self):
        self.resetar_se_novo_dia()
        return self.mensagens_hoje < self.LIMITE_DIARIO

    def registrar_envio(self):
        self.resetar_se_novo_dia()
        self.mensagens_hoje += 1
        self.save()