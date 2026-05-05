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