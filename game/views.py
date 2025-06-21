from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInfo
from lobby.models import User, Session

@csrf_exempt
def get_user_info(request):
    user_id = request.COOKIES.get("user_id")
    user = User.objects.filter(id=user_id).first()
    user_data = UserInfo.objects.filter(user=user).first()

    
    return JsonResponse(user_data.get_data_in_json())


def render_game(request):
    return render(request, "game/game.html")