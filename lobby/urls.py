from django.urls import path
from .views import render_lobby
urlpatterns = [
    path("<str:lobby_id>", render_lobby)
]


