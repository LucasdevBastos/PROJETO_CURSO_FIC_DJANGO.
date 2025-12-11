# anime/views.py
import requests
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Anime


# ===== MAPEAMENTO DE GÊNEROS PARA PT-BR =====
GENRE_TRANSLATIONS = {
    "action": "Ação",
    "adventure": "Aventura",
    "comedy": "Comédia",
    "drama": "Drama",
    "slice of life": "Slice of Life",
    "fantasy": "Fantasia",
    "horror": "Terror",
    "sci-fi": "Ficção Científica",
    "mystery": "Mistério",
    "romance": "Romance",
    "isekai": "Isekai",
    "mecha": "Mecha",
    "psychological": "Psicológico",
    "supernatural": "Sobrenatural",
    "sports": "Esportes",
    "thriller": "Suspense",
    "school": "Escolar",
    "music": "Música",
    "kids": "Infantil",
    "harem": "Harem",
    "shounen": "Shounen",
    "shoujo": "Shoujo",
    "seinen": "Seinen",
}


def get_genre_translations():
    """Retorna mapeamento de gêneros para PT-BR"""
    return GENRE_TRANSLATIONS


def translate_genre(genre_name):
    """Traduz um gênero para PT-BR"""
    if not genre_name:
        return genre_name
    return GENRE_TRANSLATIONS.get(genre_name.lower(), genre_name)


def anime_list(request):
    """
    View de listagem de animes com filtros por gênero e busca
    """
    # ===== PARÂMETROS GET =====
    query = request.GET.get('q', '').strip()
    selected_genre = request.GET.get('genre', '').strip()
    
    # ===== ANIMES DO BANCO =====
    animes_db = (
        Anime.objects
        .select_related("temporada")
        .prefetch_related("generos")
        .all()
    )
    
    # Filtrar por busca
    if query:
        animes_db = animes_db.filter(
            Q(titulo__icontains=query) | 
            Q(titulo_ingles__icontains=query) |
            Q(sinopse__icontains=query)
        )
    
    # Filtrar por gênero
    if selected_genre:
        animes_db = animes_db.filter(generos__nome__iexact=selected_genre)
    
    # ===== OBTER TODOS OS GÊNEROS DISPONÍVEIS =====
    genres_raw = (
        Anime.objects
        .prefetch_related("generos")
        .values_list("generos__nome", flat=True)
        .distinct()
        .order_by("generos__nome")
    )
    
    # Traduzir gêneros
    genres_list = []
    seen = set()
    for genre_raw in genres_raw:
        if genre_raw and genre_raw not in seen:
            genres_list.append({
                "original": genre_raw,
                "translated": translate_genre(genre_raw),
            })
            seen.add(genre_raw)
    
    # ===== FAVORITOS =====
    favoritos = []
    if request.user.is_authenticated:
        from core.models import Favorito
        from core.jikan_api import JikanAPI
        
        favoritos_ids = Favorito.objects.filter(user=request.user).values_list('anime_id', flat=True)
        for fav_id in favoritos_ids[:12]:
            anime_data = JikanAPI.get_anime_by_id(fav_id)
            if anime_data:
                favoritos.append(anime_data)
    
    # ===== PREPARAR DADOS PARA CONTEXTO =====
    animes_list = []
    for anime in animes_db:
        generos_traduzidos = [translate_genre(g.nome) for g in anime.generos.all()]
        animes_list.append({
            'id': anime.id,
            'mal_id': anime.mal_id,
            'titulo': anime.titulo,
            'titulo_ingles': anime.titulo_ingles,
            'imagem_url': anime.imagem_url,
            'sinopse': anime.sinopse,
            'nota_mal': anime.nota_mal,
            'generos': generos_traduzidos,
            'status': anime.get_status_display() if hasattr(anime, 'get_status_display') else '',
            'tipo': anime.get_tipo_display() if hasattr(anime, 'get_tipo_display') else '',
        })
    
    # ===== PAGINAÇÃO =====
    paginator = Paginator(animes_list, 20)  # 20 animes por página
    page_number = request.GET.get('page', 1)
    
    try:
        animes_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        animes_paginated = paginator.page(1)
    except EmptyPage:
        animes_paginated = paginator.page(paginator.num_pages)

    context = {
        "animes": animes_paginated,
        "favoritos": favoritos,
        "genres": genres_list,
        "selected_genre": selected_genre,
        "query": query,
        "total_animes": len(animes_list),
        "paginator": paginator,
        "page_obj": animes_paginated,
    }
    return render(request, "anime_list.html", context)
