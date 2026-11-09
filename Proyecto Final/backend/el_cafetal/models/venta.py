from django.db import models


class venta(models.Model):

    class MetodoPago(models.TextChoices):
        EFECTIVO = "EF", "Efectivo"
        TARJETA_DEBITO = "TD", "Tarjeta de Débito"
        TARJETA_CREDITO = "TC", "Tarjeta de Crédito"
        TRANSFERENCIA = "TR", "Transferencia"

    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Venta {self.id} - {self.fecha} - {self.cliente}"