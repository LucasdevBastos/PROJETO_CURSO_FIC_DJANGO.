# anime/urls.py
from django.urls import path
from . import views

app_name = "anime"

urlpatterns = [
    path("lista/", views.anime_list, name="anime_list"),
]