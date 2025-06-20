from django.urls import path
from .views import render_game, get_user_info

urlpatterns = [
    path("", render_game),
    path("info", get_user_info)
]