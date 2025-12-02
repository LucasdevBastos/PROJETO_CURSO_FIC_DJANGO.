# anime/views.py
import requests
from django.shortcuts import render
from django.db.models import Q
from .models import Anime


def anime_list(request):
    # ===== BUSCA =====
    query = request.GET.get('q', '').strip()
    
    # 1) Animes do banco
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
    
    # ===== FAVORITOS =====
    favoritos = []
    if request.user.is_authenticated:
        from core.models import Favorito
        favoritos_ids = Favorito.objects.filter(user=request.user).values_list('anime_id', flat=True)
        favoritos = animes_db.filter(mal_id__in=favoritos_ids)[:12]
    
    # ===== ANIMES POR GÊNERO (Jikan API - Carrossel) =====
    generos_carrossel = {}
    generos_list = [1, 2, 4, 5, 7, 8, 10, 14, 15, 16, 18, 19, 22, 25, 26, 28, 32, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    
    for genero_id in generos_list[:6]:  # Pega só 6 gêneros principais
        try:
            resp = requests.get(
                f"https://api.jikan.moe/v4/anime?genres={genero_id}&order_by=score&sort=desc&limit=12",
                timeout=8
            )
            resp.raise_for_status()
            data = resp.json().get("data", [])
            
            if data:
                genero_nome = data[0].get("genres", [{}])[0].get("name", f"Gênero {genero_id}")
                generos_carrossel[genero_nome] = []
                
                for item in data[:12]:
                    images = item.get("images", {}).get("jpg", {}) or {}
                    generos_carrossel[genero_nome].append({
                        "mal_id": item.get("mal_id"),
                        "titulo": item.get("title") or "Sem título",
                        "titulo_ingles": item.get("title_english"),
                        "imagem_url": images.get("image_url"),
                        "sinopse": item.get("synopsis"),
                        "nota_mal": item.get("score"),
                        "episodios": item.get("episodes"),
                        "year": item.get("year"),
                        "generos": [g.get("name") for g in item.get("genres", [])][:3],
                    })
        except Exception as e:
            print(f"Erro ao chamar Jikan API para gênero {genero_id}:", e)
    
    # ===== TEMPORADAS =====
    temporadas = {}
    temporadas_list = [
        ("fall", "2024", "Outono 2024"),
        ("summer", "2024", "Verão 2024"),
        ("spring", "2024", "Primavera 2024"),
        ("winter", "2024", "Inverno 2024"),
    ]
    
    for season, year, label in temporadas_list:
        try:
            resp = requests.get(
                f"https://api.jikan.moe/v4/seasons/{year}/{season}?limit=12",
                timeout=8
            )
            resp.raise_for_status()
            data = resp.json().get("data", [])
            
            temporadas[label] = []
            for item in data[:12]:
                images = item.get("images", {}).get("jpg", {}) or {}
                temporadas[label].append({
                    "mal_id": item.get("mal_id"),
                    "titulo": item.get("title") or "Sem título",
                    "imagem_url": images.get("image_url"),
                    "nota_mal": item.get("score"),
                    "episodios": item.get("episodes"),
                })
        except Exception as e:
            print(f"Erro ao chamar Jikan API para temporada {season} {year}:", e)
    
    # ===== TEMPORADA ATUAL =====
    animes_mal_current = []
    try:
        resp = requests.get("https://api.jikan.moe/v4/seasons/now", timeout=8)
        resp.raise_for_status()
        data = resp.json().get("data", [])

        for item in data[:12]:
            images = item.get("images", {}).get("jpg", {}) or {}
            animes_mal_current.append({
                "mal_id": item.get("mal_id"),
                "titulo": item.get("title") or "Sem título",
                "titulo_ingles": item.get("title_english"),
                "imagem_url": images.get("image_url"),
                "sinopse": item.get("synopsis"),
                "nota_mal": item.get("score"),
                "episodios": item.get("episodes"),
                "season": item.get("season"),
                "year": item.get("year"),
            })
    except Exception as e:
        print("Erro ao chamar Jikan API (temporada atual):", e)

    context = {
        "animes": animes_db,
        "animes_mal_current": animes_mal_current,
        "favoritos": favoritos,
        "generos_carrossel": generos_carrossel,
        "temporadas": temporadas,
        "query": query,
    }
    return render(request, "anime_list.html", context)
