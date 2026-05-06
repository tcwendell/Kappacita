from django.db import models
class Profissao(models.Model):
    nome = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    salario_min = models.DecimalField(max_digits=10, decimal_places=2)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2)
    icone = models.ImageField(max_length=50)
    estrelas = models.IntegerField(default=4) 

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
    avaliacao = models.IntegerField(default=4)
    icone = models.ImageField(upload_to='cursos/icones/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


class Favorito(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'curso')

    def __str__(self):
        return f'{self.usuario.username} → {self.curso.nome}'