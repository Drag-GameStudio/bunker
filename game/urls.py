from django.urls import path
from .views import render_game, get_user_info, user_is_alive

urlpatterns = [
    path("", render_game),
    path("info", get_user_info),
    path("info/isAlive", user_is_alive)
]