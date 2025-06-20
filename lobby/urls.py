from django.urls import path
from .views import render_lobby, isOwner
urlpatterns = [
    path("<int:lobby_id>", render_lobby),
    path("is_owner", isOwner)
]


