from django.db import models
from django.conf import settings


class Company(models.Model):
    nombre = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre


class Client(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200, default="")
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    # ForeignKey para relación "muchos a uno": muchos clientes pueden pertenecer a una company
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
    )
    # ForeignKey para comercial asignado a este cliente
    comercial = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="clientes_asignados",
    )
    # Graba la fecha automáticamente al crear el registro
    fecha_alta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Interaction(models.Model):
    # Limita s 3 opciones
    TIPO_CHOICES = [
        ("llamada", "Llamada"),
        ("email", "Email"),
        ("reunion", "Reunión"),
    ]
    # CASCADE: si se borra el cliente, se borran sus interacciones
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="interactions"
    )
    comercial = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="interacciones_realizadas",
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.tipo} - {self.client.nombre} - {self.fecha:%d/%m/%Y}"
