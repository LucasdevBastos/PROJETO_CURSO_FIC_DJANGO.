# calendar_app/views.py
import calendar
import logging
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import AnimeScheduleService

logger = logging.getLogger(__name__)


@login_required
def month_current(request):
    """
    Redireciona para a visualização do mês atual.
    URL: /calendario/
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
