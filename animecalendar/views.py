from datetime import datetime
from django.shortcuts import render
from core.jikan_api import JikanAPI

def landing(request):
    """
    Landing page com suporte a busca, lançamentos, populares e bem avaliados
    """
    context = {
        'today_schedule': [],
        'popular_animes': [],
        'top_rated_animes': [],
        'search_results': [],
        'search_query': '',
        'has_search': False,
        'error_message': '',
    }
    
    # 1. Busca se houver query
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        context['search_query'] = search_query
        context['has_search'] = True
        
        # Buscar animes por termo
        results = JikanAPI.search_anime(search_query, limit=12)
        
        if results:
            context['search_results'] = results
        else:
            context['error_message'] = f"Nenhum anime encontrado para '{search_query}'."
    
    # 2. Animes lançados/atualizados hoje (se não há busca)
    if not context['has_search']:
        weekday = datetime.utcnow().strftime("%A").lower()
        
        try:
            import requests
            resp = requests.get(
                "https://api.jikan.moe/v4/schedules",
                params={
                    "filter": weekday,
                    "limit": 12,
                },
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            context['today_schedule'] = data.get("data", [])
        except Exception:
            context['today_schedule'] = []
        
        # 3. Animes populares (se não há busca)
        popular = JikanAPI.get_popular_anime(limit=12, page=1)
        context['popular_animes'] = popular
        
        # 4. Animes bem avaliados (se não há busca)
        top_rated = JikanAPI.get_top_anime(limit=12, page=1)
        context['top_rated_animes'] = top_rated
    
    return render(request, 'landing.html', context)