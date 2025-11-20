# calendar_app/views.py
import calendar
from datetime import date, timedelta

from django.shortcuts import render
from django.utils import timezone

# Tenta importar Airing, mas não quebra se não existir
try:
    from anime.models import Airing  # ajusta depois se o nome for outro
except ImportError:
    Airing = None

def month_view(request, year=None, month=None):
    # Se não vier ano/mês na URL, usa o mês atual
    today = timezone.localdate()

    if year is None or month is None:
        year = today.year
        month = today.month

    year = int(year)
    month = int(month)

    # Primeiro e último dia do mês
    first_day = date(year, month, 1)
    _, last_day_in_month = calendar.monthrange(year, month)
    last_day = date(year, month, last_day_in_month)

    # Dicionário de exibições por data
    airings_by_date = {}

    # Só tenta buscar no banco se o modelo existir
    if Airing is not None:
        airings_qs = (
            Airing.objects.select_related("anime")
            .filter(data_exibicao__range=(first_day, last_day))
            .order_by("data_exibicao", "hora_exibicao")
        )

        for airing in airings_qs:
            airings_by_date.setdefault(airing.data_exibicao, []).append(airing)

    # Monta as semanas do calendário
    cal = calendar.Calendar(firstweekday=0)  # 0 = segunda
    month_weeks = cal.monthdatescalendar(year, month)

    weeks = []
    for week in month_weeks:
        week_data = []
        for day in week:
            week_data.append(
                {
                    "date": day,
                    "in_month": day.month == month,
                    "is_today": day == today,
                    "airings": airings_by_date.get(day, []),
                }
            )
        weeks.append(week_data)

    prev_month_date = first_day - timedelta(days=1)
    next_month_date = last_day + timedelta(days=1)

    context = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "weeks": weeks,
        "today": today,
        "prev_year": prev_month_date.year,
        "prev_month": prev_month_date.month,
        "next_year": next_month_date.year,
        "next_month": next_month_date.month,
    }

    return render(request, "calendar_app/month.html", context)
