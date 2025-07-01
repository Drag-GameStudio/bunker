from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User, Session
from django.views.decorators.csrf import csrf_exempt
from bunker.settings import MIDDLELINK

# Create your views here.
def render_lobby(request, lobby_id):
    """
    Render the lobby page.
    """

    user_id = request.COOKIES.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return HttpResponse("User not found.", status=404)
    
    if int(lobby_id) == user.session.id:
        return render(request, "lobby/lobby.html", {"lobby_id": lobby_id, "MIDDLELINK": MIDDLELINK})
    
    return HttpResponse("You are not allowed to view this lobby.", status=403)

@csrf_exempt
def isOwner(request):

    user_id = request.COOKIES.get("user_id")
    user = User.objects.filter(id=user_id).first()

    return JsonResponse({"isOwner": user.isOwner})
    