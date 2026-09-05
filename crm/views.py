from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q  # Q permite armar condiciones OR/AND complejas
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from .models import Client, Interaction, Company

from .forms import (
    ClientForm,
    InteractionForm,
    ComercialForm,
    ComercialUpdateForm,
    CompanyForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class LoginRequiredView(LoginRequiredMixin):
    # Cualquier vista que herede de esta exige login
    login_url = "login"
    redirect_field_name = "next"


class AdminRequiredView(LoginRequiredView, UserPassesTestMixin):
    # Hereda login obligatorio y agrega una verificación extra (test_func)
    def test_func(self):
        return self.request.user.is_staff


# ---- Vistas de Client ----


class ClientListView(LoginRequiredView, ListView):
    model = Client
    template_name = "crm/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        # Filtrar según la búsqueda
        query = self.request.GET.get("q", "")
        if query:
            return Client.objects.filter(
                Q(nombre__icontains=query)
                | Q(apellido__icontains=query)
                | Q(email__icontains=query)
                | Q(company__nombre__icontains=query)
            )
        return Client.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class ClientDetailView(LoginRequiredView, DetailView):
    model = Client
    template_name = "crm/client_detail.html"
    context_object_name = "client"


class ClientCreateView(LoginRequiredView, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"
    success_url = reverse_lazy("client_list")


class ClientUpdateView(LoginRequiredView, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"
    success_url = reverse_lazy("client_list")


class ClientDeleteView(LoginRequiredView, DeleteView):
    model = Client
    template_name = "crm/client_confirm_delete.html"
    success_url = reverse_lazy("client_list")


# ---- Vistas de Empresa ----


class CompanyListView(LoginRequiredView, ListView):
    model = Company
    template_name = "crm/company_list.html"
    context_object_name = "companies"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return Company.objects.filter(
                Q(nombre__icontains=query) | Q(sector__icontains=query)
            )
        return Company.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class CompanyDetailView(LoginRequiredView, DetailView):
    model = Company
    template_name = "crm/company_detail.html"
    context_object_name = "company"


class CompanyCreateView(LoginRequiredView, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "crm/company_form.html"
    success_url = reverse_lazy("company_list")


class CompanyUpdateView(LoginRequiredView, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "crm/company_form.html"
    success_url = reverse_lazy("company_list")


class CompanyDeleteView(LoginRequiredView, DeleteView):
    model = Company
    template_name = "crm/company_confirm_delete.html"
    success_url = reverse_lazy("company_list")


# ---- Vistas de Interaction ----


class InteractionCreateView(LoginRequiredView, CreateView):
    model = Interaction
    form_class = InteractionForm
    template_name = "crm/interaction_form.html"

    def form_valid(self, form):
        client = get_object_or_404(Client, pk=self.kwargs["client_pk"])
        form.instance.client = client
        self.client_obj = client
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("client_detail", kwargs={"pk": self.client_obj.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = get_object_or_404(Client, pk=self.kwargs["client_pk"])
        return context


class InteractionDeleteView(LoginRequiredView, DeleteView):
    model = Interaction
    template_name = "crm/interaction_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("client_detail", kwargs={"pk": self.object.client.pk})


# ---- Vistas de Comercial ----


class ComercialListView(AdminRequiredView, ListView):
    model = User
    template_name = "crm/comercial_list.html"
    context_object_name = "comerciales"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        base = User.objects.filter(is_staff=False).order_by("username")
        base = User.objects.all().order_by("username")
        if query:
            return base.filter(
                Q(username__icontains=query)
                | Q(email__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )
        return base

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class ComercialCreateView(AdminRequiredView, CreateView):
    model = User
    form_class = ComercialForm
    template_name = "crm/comercial_form.html"
    success_url = reverse_lazy("comercial_list")


class ComercialUpdateView(AdminRequiredView, UpdateView):
    model = User
    form_class = ComercialUpdateForm
    template_name = "crm/comercial_form.html"
    success_url = reverse_lazy("comercial_list")


class ComercialDeactivateView(AdminRequiredView, UpdateView):
    model = User
    fields = []  # No muestra campos editables. Solo pide confirmación
    template_name = "crm/comercial_confirm_deactivate.html"
    success_url = reverse_lazy("comercial_list")

    def form_valid(self, form):
        form.instance.is_active = False
        return super().form_valid(form)


class MenuView(LoginRequiredView, TemplateView):
    template_name = "crm/menu.html"
