# anime/views.py
import requests
from django.shortcuts import render
from .models import Anime


def anime_list(request):
    # 1) Animes do banco (já existia)
    animes_db = (
        Anime.objects
        .select_related("temporada")
        .prefetch_related("generos")
        .all()
    )

    # 2) Animes da MyAnimeList via Jikan API
    animes_mal = []
    try:
        # Temporada atual
        resp = requests.get("https://api.jikan.moe/v4/seasons/now", timeout=8)
        resp.raise_for_status()
        data = resp.json().get("data", [])

        for item in data[:12]:  # pega só 12 pra testar
            images = item.get("images", {}).get("jpg", {}) or {}
            animes_mal.append({
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
        # Só pra debug no terminal
        print("Erro ao chamar Jikan API:", e)

    context = {
        "animes": animes_db,
        "animes_mal": animes_mal,
    }
    return render(request, "anime_list.html", context)
