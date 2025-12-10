# calendar_app/views.py
import calendar
import logging
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import AnimeScheduleService

logger = logging.getLogger(__name__)


@login_required
def calendario_semanal(request):
    """
    Mostra o calendário semanal com animes organizados por dia da semana.
    Usa a Jikan API para buscar os animes de cada dia.
    URL: /calendario/
    """
    logger.info("[CALENDARIO SEMANAL] Buscando dados da Jikan API...")
    
    # Busca animes para cada dia da semana
    calendario = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": [],
    }
    
    # Para cada dia da semana, busca os animes e faz parse
    for weekday_name in calendario.keys():
        try:
            animes = AnimeScheduleService.get_animes_by_weekday(weekday_name)
            # Faz parse dos dados
            calendario[weekday_name] = [
                AnimeScheduleService.parse_anime_data(anime)
                for anime in animes
            ]
            logger.info(f"[{weekday_name.upper()}] {len(calendario[weekday_name])} animes encontrados")
        except Exception as e:
            logger.error(f"[ERRO] Falha ao buscar animes de {weekday_name}: {str(e)}")
            calendario[weekday_name] = []
    
    context = {
        "calendario": calendario,
    }
    
    return render(request, "calendar_app/calendario.html", context)


@login_required
def month_current(request):
    """
    Redireciona para a visualização do mês atual.
    URL: /calendario/mes/
    """
    today = date.today()
    return month_view(request, year=today.year, month=today.month)


@login_required
def month_view(request, year, month):
    """
    Mostra o calendário de um mês específico com dados da Jikan API.
    URL: /calendario/<year>/<month>/
    """
    today = date.today()

    # Gera as semanas do mês com dados da API
    cal = calendar.Calendar(firstweekday=0)  # 0 = Monday
    month_dates = cal.monthdatescalendar(year, month)

    weeks = []
    for week in month_dates:
        week_data = []
        for d in week:
            # Busca animes para este dia da Jikan API
            day_animes = AnimeScheduleService.get_animes_for_calendar_day(d, parse=True)
            
            # Limita a 5 animes por dia para não ficar muito poluído
            day_animes = day_animes[:5]

            week_data.append({
                "date": d,
                "in_month": d.month == month,
                "is_today": (d == today),
                "animes": day_animes,  # Mudei de "airings" para "animes"
                "anime_count": len(day_animes),  # Quantidade total de animes
            })
        weeks.append(week_data)

    # Navegação mês anterior / próximo
    first_day = date(year, month, 1)
    prev_date = first_day - timedelta(days=1)
    prev_year, prev_month = prev_date.year, prev_date.month

    last_day = date(year, month, calendar.monthrange(year, month)[1])
    next_date = last_day + timedelta(days=1)
    next_year, next_month = next_date.year, next_date.month

    context = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "weeks": weeks,
        "today": today,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    }
    
    logger.info(f"[CALENDAR] Renderizando calendário para {month}/{year}")
    return render(request, "calendar_app/month.html", context)
