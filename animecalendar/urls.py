# animecalendar/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("animes/", include("anime.urls")),
    path("comentarios/", include("comments.urls")),
    path("conta/", include("users.urls")),
    # core/calendar etc. você adiciona conforme for criando as views
]
