# calendar_app/views.py
import calendar
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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
    Mostra o calendário de um mês específico.
    URL: /calendario/<year>/<month>/
    """
    today = date.today()

    # Gera as semanas do mês (com dias completos, incluindo "sobra" do mês anterior/seguinte)
    cal = calendar.Calendar(firstweekday=0)  # 0 = segunda? 0 = Monday (na doc), mas no BR normalmente 0 = Monday; se quiser domingo como início, usa 6.
    month_dates = cal.monthdatescalendar(year, month)

    weeks = []
    for week in month_dates:
        week_data = []
        for d in week:
            # aqui futuramente você vai buscar os episódios do dia "d"
            # ex: Airing.objects.filter(airing_time__date=d)
            day_airings = []

            week_data.append({
                "date": d,
                "in_month": d.month == month,
                "is_today": (d == today),
                "airings": day_airings,
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
    return render(request, "calendar_app/month.html", context)
