from django.urls import path
from .views import render_menu, login_user, connect_to_session, create_session

urlpatterns = [
    path("", render_menu),
    path("login_user", login_user),
    path("connect_to_session", connect_to_session), 
    path("create_session", create_session),
]