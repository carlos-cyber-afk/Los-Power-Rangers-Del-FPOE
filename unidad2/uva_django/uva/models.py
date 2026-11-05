from django.db import models

class Uva (models.Model):
    tamano = models.IntegerField()
    peso = models.FloatField()
    forma = models.CharField(max_length=50)
    textura = models.CharField(max_length=50)

    def __str__(self):
        return f"Uva {self.forma} - tamaño:{self.tamano} - textura:{self.textura} - peso:{self.peso}"

# Create your models here.
