from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Client, Interaction, Company


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["nombre", "apellido", "email", "telefono", "company", "comercial"]


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["nombre", "sector", "direccion", "telefono"]


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        # "client" NO va en la lista de fields porque el cliente se asigna desde url
        fields = ["tipo", "comercial", "notas"]


class ComercialForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(required=False, label="¿Es administrador?")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name", "is_staff"]


class ComercialUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "is_staff"]
