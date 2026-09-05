from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),
    path("clients/nuevo/", views.ClientCreateView.as_view(), name="client_create"),
    path(
        "clients/<int:pk>/editar/",
        views.ClientUpdateView.as_view(),
        name="client_update",
    ),
    path(
        "clients/<int:pk>/borrar/",
        views.ClientDeleteView.as_view(),
        name="client_delete",
    ),
    path(
        "clients/<int:client_pk>/interacciones/nueva/",
        views.InteractionCreateView.as_view(),
        name="interaction_create",
    ),
    path("companies/", views.CompanyListView.as_view(), name="company_list"),
    path(
        "companies/<int:pk>/", views.CompanyDetailView.as_view(), name="company_detail"
    ),
    path("companies/nuevo/", views.CompanyCreateView.as_view(), name="company_create"),
    path(
        "companies/<int:pk>/editar/",
        views.CompanyUpdateView.as_view(),
        name="company_update",
    ),
    path(
        "companies/<int:pk>/borrar/",
        views.CompanyDeleteView.as_view(),
        name="company_delete",
    ),
    path(
        "interacciones/<int:pk>/borrar/",
        views.InteractionDeleteView.as_view(),
        name="interaction_delete",
    ),
    path("comerciales/", views.ComercialListView.as_view(), name="comercial_list"),
    path(
        "comerciales/nuevo/",
        views.ComercialCreateView.as_view(),
        name="comercial_create",
    ),
    path(
        "comerciales/<int:pk>/editar/",
        views.ComercialUpdateView.as_view(),
        name="comercial_update",
    ),
    path(
        "comerciales/<int:pk>/desactivar/",
        views.ComercialDeactivateView.as_view(),
        name="comercial_deactivate",
    ),
    path("menu/", views.MenuView.as_view(), name="menu"),
    path("estadisticas/", views.StatsView.as_view(), name="stats"),
    path("clients/exportar/", views.ClientExportView.as_view(), name="client_export"),
    path(
        "interacciones/exportar/",
        views.InteractionExportView.as_view(),
        name="interaction_export",
    ),
]
