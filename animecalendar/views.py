import requests
from datetime import datetime
from django.shortcuts import render

def landing(request):
    # Dia da semana em inglês, minúsculo (monday, tuesday, etc.)
    weekday = datetime.utcnow().strftime("%A").lower()

    animes_hoje = []

    try:
        # Endpoint de horários da Jikan (unofficial MyAnimeList)
        resp = requests.get(
            "https://api.jikan.moe/v4/schedules",
            params={
                "filter": weekday,  # dia (monday, tuesday...)
                "limit": 12,        # quantos animes trazer
            },
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        animes_hoje = data.get("data", [])
    except Exception:
        # Se der erro na API, só não mostra nada (evita quebrar a página)
        animes_hoje = []

    context = {
        "today_schedule": animes_hoje,
    }
    return render(request, "landing.html", context)