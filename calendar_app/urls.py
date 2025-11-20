from django.urls import path
from . import views

app_name = "calendar_app"

urlpatterns = [
    path("", views.month_view, name="month_current"),
    path("<int:year>/<int:month>/", views.month_view, name="month_by_date"),
]
