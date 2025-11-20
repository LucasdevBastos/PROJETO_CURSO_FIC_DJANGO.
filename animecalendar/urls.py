# animecalendar/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views  # importa a landing

urlpatterns = [
    path("", views.landing, name="landing"),  # ← landing como página inicial
    path("admin/", admin.site.urls),
    path("animes/", include("anime.urls")),
    path("comentarios/", include("comments.urls")),
    path("conta/", include("users.urls")),
    path("calendario/", include("calendar_app.urls")),  # calendário
]
