"""
URL principales del proyecto.

- /admin/  Panel de administración de Django.
- /api/    REST API de la app Biblioteca.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("Biblioteca.urls")),
]
