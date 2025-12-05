# animecalendar/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # importa a landing

urlpatterns = [
    path("", views.landing, name="landing"),  # ← landing como página inicial
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # URLs padrão de autenticação
    path("core/", include("core.urls")),  # core app (anime detail, favoritos)
    path("animes/", include("anime.urls")),
    path("comentario/", include("comentarios.urls")),  # novo app comentarios
    path("perfil/", include("perfil.urls")),  # novo app perfil
    path("comentarios/", include("comments.urls")),  # comments (original)
    path("conta/", include("users.urls")),
    path("calendario/", include("calendar_app.urls")),  # calendário
]

# Servir media files em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
