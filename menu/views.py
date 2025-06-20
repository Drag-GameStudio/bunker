from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from lobby.models import User, Session
from django.views.decorators.csrf import csrf_exempt
import json
from bunker.settings import VARIABLE_OF_STATE

# Create your views here.
def render_menu(request):
    """
    Render the menu page.
    """
    return render(request, "menu/menu.html")

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        user = User(username=username)
        user.save()

        response = HttpResponse("User created successfully")
        response.set_cookie("user_id", user.id, max_age=3600)
        

        return response
    
    return HttpResponse("Invalid request method", status=405)

@csrf_exempt
def connect_to_session(request):
    if request.method == "POST":
        user_id = request.COOKIES.get("user_id")

        data = json.loads(request.body)
        session_id = data.get("session_id")


        try:
            user = User.objects.get(id=user_id)
            session = Session.objects.get(id=session_id)
            if session.state == VARIABLE_OF_STATE[0]:

                user.session = session
                user.save()

                return HttpResponse(f"User {user.username} connected to session {session.id}")
            
            return HttpResponse(f"session have been started")
            
        except User.DoesNotExist:
            return HttpResponse("User does not exist", status=404)
        except Session.DoesNotExist:
            return HttpResponse("Session does not exist", status=404)

    return HttpResponse("Invalid request method", status=405)

@csrf_exempt
def create_session(request):
    if request.method == "POST":
        user_id = request.COOKIES.get("user_id")

        session = Session()
        session.save()
        user = User.objects.filter(id=user_id).first()
        user.isOwner = True
        user.save()

        return JsonResponse({"session_id": session.id})

    return HttpResponse("Invalid request method", status=405)