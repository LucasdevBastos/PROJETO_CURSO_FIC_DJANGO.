"""
Utilitários para consumir a API Jikan (MyAnimeList)
"""
import requests
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class JikanAPI:
    """Classe para consumir a API Jikan v4"""
    
    BASE_URL = "https://api.jikan.moe/v4"
    TIMEOUT = 5
    CACHE_TTL = 3600 * 4  # 4 horas
    
    @staticmethod
    def _make_request(endpoint, params=None):
        """
        Faz requisição HTTP segura com cache
        """
        try:
            url = f"{JikanAPI.BASE_URL}{endpoint}"
            response = requests.get(
                url,
                params=params,
                timeout=JikanAPI.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            logger.warning(f"[TIMEOUT] Jikan API timeout: {endpoint}")
            return {}
        except requests.ConnectionError:
            logger.warning(f"[CONNECTION] Jikan API connection error: {endpoint}")
            return {}
        except Exception as e:
            logger.error(f"[ERROR] Jikan API error: {str(e)}")
            return {}
    
    @staticmethod
    def get_anime_by_id(anime_id):
        """
        Busca anime completo por ID com cache
        """
        cache_key = f"jikan_anime_{anime_id}"
        
        # Tenta pegar do cache
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"[CACHE HIT] anime_id={anime_id}")
            return cached
        
        # Faz requisição à API
        logger.info(f"[API CALL] anime_id={anime_id}")
        data = JikanAPI._make_request(f"/anime/{anime_id}/full")
        
        if data.get('data'):
            # Armazena em cache
            cache.set(cache_key, data['data'], JikanAPI.CACHE_TTL)
            logger.info(f"[SUCCESS] anime_id={anime_id}")
            return data['data']
        
        logger.warning(f"[WARNING] anime_id={anime_id} not found")
        return None
    
    @staticmethod
    def get_anime_news(anime_id, limit=5):
        """
        Busca notícias sobre um anime
        """
        try:
            data = JikanAPI._make_request(f"/anime/{anime_id}/news", {'limit': limit})
            return data.get('data', [])
        except Exception as e:
            logger.error(f"[ERROR] get_anime_news: {str(e)}")
            return []
    
    @staticmethod
    def get_anime_characters(anime_id, limit=10):
        """
        Busca personagens de um anime
        """
        try:
            data = JikanAPI._make_request(f"/anime/{anime_id}/characters")
            characters = data.get('data', [])[:limit]
            return characters
        except Exception as e:
            logger.error(f"[ERROR] get_anime_characters: {str(e)}")
            return []
    
    @staticmethod
    def get_anime_reviews(anime_id, limit=5):
        """
        Busca reviews de um anime
        """
        try:
            data = JikanAPI._make_request(f"/anime/{anime_id}/reviews")
            reviews = data.get('data', [])[:limit]
            return reviews
        except Exception as e:
            logger.error(f"[ERROR] get_anime_reviews: {str(e)}")
            return []
    
    @staticmethod
    def get_top_anime(limit=25, page=1):
        """
        Busca animes mais bem classificados com cache
        """
        cache_key = f"jikan_top_anime_{limit}_{page}"
        
        # Tenta pegar do cache
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"[CACHE HIT] top_anime page={page}")
            return cached
        
        # Faz requisição à API
        logger.info(f"[API CALL] top_anime page={page}")
        data = JikanAPI._make_request(
            "/top/anime",
            {'limit': limit, 'page': page}
        )
        
        if data.get('data'):
            # Armazena em cache
            cache.set(cache_key, data['data'], JikanAPI.CACHE_TTL)
            logger.info(f"[SUCCESS] top_anime page={page}")
            return data['data']
        
        logger.warning(f"[WARNING] top_anime page={page} empty")
        return []
    
    @staticmethod
    def search_anime(query, limit=20):
        """
        Busca animes por nome/query com cache
        """
        cache_key = f"jikan_search_{query}_{limit}"
        
        # Tenta pegar do cache
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"[CACHE HIT] search_anime query={query}")
            return cached
        
        # Faz requisição à API
        logger.info(f"[API CALL] search_anime query={query}")
        data = JikanAPI._make_request(
            "/anime",
            {'query': query, 'limit': limit}
        )
        
        if data.get('data'):
            # Armazena em cache
            cache.set(cache_key, data['data'], JikanAPI.CACHE_TTL)
            logger.info(f"[SUCCESS] search_anime query={query} found={len(data['data'])}")
            return data['data']
        
        logger.warning(f"[WARNING] search_anime query={query} empty")
        return []
    
    @staticmethod
    def get_popular_anime(limit=25, page=1):
        """
        Busca animes populares com cache
        """
        cache_key = f"jikan_popular_anime_{limit}_{page}"
        
        # Tenta pegar do cache
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"[CACHE HIT] popular_anime page={page}")
            return cached
        
        # Faz requisição à API usando endpoint de top/popular
        logger.info(f"[API CALL] popular_anime page={page}")
        data = JikanAPI._make_request(
            "/top/anime",
            {'limit': limit, 'page': page, 'filter': 'bypopularity'}
        )
        
        if data.get('data'):
            # Armazena em cache
            cache.set(cache_key, data['data'], JikanAPI.CACHE_TTL)
            logger.info(f"[SUCCESS] popular_anime page={page}")
            return data['data']
        
        logger.warning(f"[WARNING] popular_anime page={page} empty")
        return []
