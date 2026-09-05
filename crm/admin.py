from django.contrib import admin
from .models import Company, Client, Interaction


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sector", "telefono")
    # Barra de búsqueda que filtra por nombre
    search_fields = ("nombre",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "company", "comercial", "fecha_alta")
    # Filtros laterales
    list_filter = ("company", "comercial")
    search_fields = ("nombre", "email")


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ("client", "tipo", "comercial", "fecha")
    list_filter = ("tipo", "comercial")
    ordering = ("-fecha",)
