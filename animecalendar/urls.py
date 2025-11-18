# animecalendar/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("animes/", include("anime.urls")),
    path("comentarios/", include("comments.urls")),  # <– assim
    path("conta/", include("users.urls")),
    
]
