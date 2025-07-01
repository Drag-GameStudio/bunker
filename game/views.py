from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInfo
from lobby.models import User, Session
from bunker.settings import MIDDLELINK

@csrf_exempt
def get_user_info(request):
    user_id = request.COOKIES.get("user_id")
    user = User.objects.filter(id=user_id).first()
    user_data = UserInfo.objects.filter(user=user).first()

    
    return JsonResponse(user_data.get_data_in_json())

@csrf_exempt
def user_is_alive(request):
    user_id = request.COOKIES.get("user_id")
    user = User.objects.filter(id=user_id).first()
    
    return JsonResponse({"isAlive": user.isAlive})


def render_game(request):
    user_id = request.COOKIES.get("user_id")
    user = User.objects.filter(id=user_id).first()

    return render(request, "game/game.html", context={"MIDDLELINK": MIDDLELINK, "situation": user.session.situation})