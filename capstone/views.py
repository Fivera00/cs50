from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render, resolve_url
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
    games = Games.objects.all()
    context = {
        'games': games
    }
    return render(request, 'capstone/index.html', context)

def categories(request, categories):
    _categories = Categories.objects.all() 
    context = {
        'categories': _categories
    }
    return render(request, 'capstone/categories.html', context)

def games(request):
    if request.method == "GET":
        return render(request, 'capstone/questions.html')
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def deleteGame(request, game):
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)
    
    _game = Games.objects.get(id=game)

    print(_game)
    if _game is None:
        return JsonResponse({"error": "Game not found."}, status=404)
    
    _game.delete()
    return JsonResponse({"message": "Game deleted successfully."}, status=201)

@csrf_exempt
@login_required
def createGame(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    game = data.get("game", "")
    if game == "":
        return JsonResponse({"error": "Missing required fields."}, status=400)
    try:
        game = Games(name=game)
        game.save()
    except IntegrityError:
        return JsonResponse({"error": "Game already exists."}, status=400)
    return JsonResponse({"message": "Game created successfully."}, status=201)

#API urls
def getGames(request):
    _games = Games.objects.all()
    return JsonResponse([Games.serialize() for Games in _games], safe=False)

def getCategories(request):
    _categories = Categories.objects.all()
    return JsonResponse([Categories.serialize() for Categories in _categories], safe=False)

def getChallenges(request):
    _challenges = Challenge.objects.all()
    return JsonResponse([Challenge.serialize() for Challenge in _challenges], safe=False)

def getChallengesByCategory(request, category):
    _challenges = Challenge.objects.filter(categoryChallenge=category)
    return JsonResponse([Challenge.serialize() for Challenge in _challenges], safe=False)

def getChallengesByGame(request, game):
    _challenges = Challenge.objects.filter(gameChallenge=game)
    return JsonResponse([Challenge.serialize() for Challenge in _challenges], safe=False)

def getChallengesByGameAndCategory(request, game, category):
    _challenges = Challenge.objects.filter(gameChallenge=game, categoryChallenge=category)
    return JsonResponse([Challenge.serialize() for Challenge in _challenges], safe=False)
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")
        
 