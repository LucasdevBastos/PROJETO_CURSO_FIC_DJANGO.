# calendar_app/urls.py
from django.urls import path
from . import views

app_name = "calendar_app"

urlpatterns = [
    # Calendário semanal (padrão) - /calendario/
    path("", views.calendario_semanal, name="calendario_semanal"),
    
    # Calendário mensal - /calendario/mes/
    path("mes/", views.month_current, name="month_current"),
    path("mes/<int:year>/<int:month>/", views.month_view, name="month_view"),
]

