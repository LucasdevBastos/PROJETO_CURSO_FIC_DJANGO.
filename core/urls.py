# core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # Anime detail
    path('anime/<int:anime_id>/', views.anime_detail, name='anime_detail'),
    
    # Favoritos
    path('anime/<int:anime_id>/favoritar/', views.toggle_favorito, name='toggle_favorito'),
    path('meus-favoritos/', views.listar_favoritos, name='meus_favoritos'),
]
