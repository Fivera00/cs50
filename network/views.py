import json
from typing import Tuple
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render, resolve_url
from django.db.models import F
from django.http import JsonResponse, response
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .models import *

@csrf_exempt
@login_required(login_url='/login')
def index(request):
    post = Post.objects.all().order_by('-date')
    allpost = paginate(request, post)

    context = {
        'allposts': allpost,
        'postLiked': "0"
    }
    return render(request, "network/index.html", context)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
 
@csrf_exempt
@login_required(login_url='/login')
def save_update_post(request):
    if request.method == "POST":
        # obtemos el json enviado desde el frontend
        data = json.loads(request.body)
        print(data)
        user_created = User.objects.get(pk = request.user.id)
        content_post = data.get("content_post")
        # creamos nuestra publicacion
        create_post = Post.objects.create(
            user = user_created,
            content = content_post
        )
        create_post.save()
        return JsonResponse({"message": "Post successfully created"}, status = 201)

    elif request.method == "PUT":
        data = json.loads(request.body)
        post_id = int(data.get("post_id"))
        content_modified = data.get("content_modified")
        user_modified_post = request.user.id
        
        post = Post.objects.get(pk = post_id)

        # Validar que solo el creador del post pueda modificar
        if post.user.id != user_modified_post:
            return JsonResponse({"message": "You aren't authorized to modify this post"}, status=403)

        post.content = content_modified
        post.save
        return JsonResponse({"message": "Post successfully updated"}, status = 201)
    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)
    

@csrf_exempt
@login_required(login_url='/login')
def likeDislike(request, postId):
    post = Post.objects.get(pk = postId)
    user = User.objects.get(pk = request.user.id)
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    post.save()
    num_likes = post.likes.count()
    return JsonResponse({"liked": liked, "num_likes": num_likes})
    

# Funciones
@csrf_exempt
@login_required(login_url='/login')
def getMyLikedPost(request):
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        
    else:
        return HttpResponseRedirect(reverse("network:login"))

# funcion para crear paginas para los post  
def paginate(request,argument):
    page_number = request.GET.get('page',1)
    paginator = Paginator(argument, 10) 

    try:
        paginated_argument = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_argument = paginator.page(1)
    except EmptyPage:
        paginated_argument = paginator.page(paginator.num_pages)
    
    return paginated_argument