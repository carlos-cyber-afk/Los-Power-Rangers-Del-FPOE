from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    paginas = models.PositiveIntegerField()
    fecha_publicacion = models.DateField()
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo