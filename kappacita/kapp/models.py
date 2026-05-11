from django.db import models
from django.contrib.auth.models import User


class Profissao(models.Model):
    nome = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, default='')
    salario_min = models.DecimalField(max_digits=10, decimal_places=2)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2)
    icone = models.ImageField(blank=True, null=True)
    avaliacao = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='categorias/', blank=True, null=True)

    def __str__(self):
        return self.nome


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    descricao = models.TextField()
    avaliacao = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    icone = models.ImageField(upload_to='cursos/icones/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


class Favorito(models.Model):
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE)
    curso     = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    profissao = models.ForeignKey(Profissao, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        # Garante que o mesmo usuário não favorite o mesmo curso ou profissão duas vezes
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