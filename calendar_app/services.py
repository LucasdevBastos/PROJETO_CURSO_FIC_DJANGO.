"""
calendar_app/services.py
Serviço de integração com Jikan API para obter animes por dia
"""
import requests
import logging
from datetime import datetime, date
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Mapeamento de dias da semana em português para inglês (Jikan API)
WEEKDAY_MAP = {
    0: "monday",     # Segunda
    1: "tuesday",    # Terça
    2: "wednesday",  # Quarta
    3: "thursday",   # Quinta
    4: "friday",     # Sexta
    5: "saturday",   # Sábado
    6: "sunday",     # Domingo
}

JIKAN_SCHEDULE_URL = "https://api.jikan.moe/v4/schedules"
JIKAN_TIMEOUT = 5
CACHE_DURATION = 3600 * 4  # 4 horas


class AnimeScheduleService:
    """
    Serviço para buscar agenda de animes da Jikan API.
    Integramos com cache para evitar sobrecarregar a API.
    """
    
    @staticmethod
    def get_animes_by_weekday(weekday_name: str) -> list:
        """
        Obtém animes que lançam em um dia específico da semana.
        
        Args:
            weekday_name: Nome do dia em inglês (monday, tuesday, etc.)
        
        Returns:
            List de dicts com dados dos animes
        """
        cache_key = f"jikan_schedule_{weekday_name}"
        
        # Tenta obter do cache primeiro
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.info(f"[CACHE HIT] Agenda para {weekday_name}")
            return cached_data
        
        try:
            logger.info(f"[API CALL] Buscando agenda para {weekday_name}")
            response = requests.get(
                JIKAN_SCHEDULE_URL,
                params={
                    "filter": weekday_name,
                    "limit": 25,  # Aumentei de 12 para 25
                    "page": 1,
                },
                timeout=JIKAN_TIMEOUT,
            )
            response.raise_for_status()
            
            data = response.json()
            animes = data.get("data", [])
            
            # Cachea os resultados
            cache.set(cache_key, animes, CACHE_DURATION)
            logger.info(f"[SUCCESS] {len(animes)} animes encontrados para {weekday_name}")
            
            return animes
            
        except requests.exceptions.Timeout:
            logger.error(f"[TIMEOUT] Jikan API timeout para {weekday_name}")
            return []
        except requests.exceptions.ConnectionError:
            logger.error(f"[CONNECTION ERROR] Falha ao conectar com Jikan API")
            return []
        except Exception as e:
            logger.error(f"[ERROR] Erro ao buscar agenda: {str(e)}")
            return []
    
    @staticmethod
    def get_animes_by_date(target_date: date) -> list:
        """
        Obtém animes que lançam em uma data específica.
        
        Args:
            target_date: Data alvo (date object)
        
        Returns:
            List de dicts com dados dos animes
        """
        # Obtém o dia da semana (0=Monday, 6=Sunday)
        weekday_num = target_date.weekday()
        weekday_name = WEEKDAY_MAP[weekday_num]
        
        return AnimeScheduleService.get_animes_by_weekday(weekday_name)
    
    @staticmethod
    def parse_anime_data(anime: dict) -> dict:
        """
        Extrai informações importantes do anime retornado pela API.
        
        Args:
            anime: Dict com dados brutos da Jikan API
        
        Returns:
            Dict com informações parseadas
        """
        try:
            # Extrai broadcast info
            broadcast = anime.get("broadcast", {})
            broadcast_string = broadcast.get("string", "")
            broadcast_time = broadcast_string.split(" at ")[-1] if "at" in broadcast_string else None
            
            # Extrai imagem
            images = anime.get("images", {})
            image_url = (
                images.get("jpg", {}).get("large_image_url") or
                images.get("jpg", {}).get("image_url") or
                ""
            )
            
            # Extrai score
            score = anime.get("score", None)
            
            return {
                "mal_id": anime.get("mal_id", 0),
                "title": anime.get("title", "Desconhecido"),
                "title_english": anime.get("title_english", ""),
                "image_url": image_url,
                "synopsis": anime.get("synopsis", "")[:200],  # Primeiros 200 chars
                "episodes": anime.get("episodes", 0),
                "status": anime.get("status", ""),
                "aired": anime.get("aired", {}).get("string", ""),
                "type": anime.get("type", ""),
                "score": score,
                "broadcast_string": broadcast_string,
                "broadcast_time": broadcast_time,
                "source": anime.get("source", ""),
                "url": anime.get("url", ""),
                "rank": anime.get("rank", None),
            }
        except Exception as e:
            logger.error(f"[PARSE ERROR] Erro ao fazer parse do anime: {str(e)}")
            return {}
    
    @staticmethod
    def get_animes_for_calendar_day(target_date: date, parse: bool = True) -> list:
        """
        Obtém animes formatados para exibição no calendário.
        
        Args:
            target_date: Data alvo
            parse: Se deve fazer parse dos dados
        
        Returns:
            List de dicts com animes formatados
        """
        animes = AnimeScheduleService.get_animes_by_date(target_date)
        
        if parse:
            animes = [
                AnimeScheduleService.parse_anime_data(anime)
                for anime in animes
            ]
        
        return animes


class CacheService:
    """
    Serviço para gerenciar cache da aplicação.
    """
    
    @staticmethod
    def clear_schedule_cache():
        """
        Limpa todo o cache de agenda.
        Útil para forçar atualização dos dados.
        """
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in weekdays:
            cache.delete(f"jikan_schedule_{day}")
        logger.info("[CACHE] Cache de agenda limpo")
