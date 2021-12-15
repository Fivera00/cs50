from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def index(request):
    listing = Auctions.objects.filter(isActiveAuction = True)
    categories = Categories.objects.all()
    #SI no hay usuario logueado se muestra solo dos campos
    if request.user.id is None:
        context = {
            'categories': categories,
            'listingAuction': listing
        }
        return render(request, "auctions/index.html", context)
    watchlist = Watchlist.objects.filter(userWatchlist = request.user)
    
    #Si hay usuario logueado, se muestra la lista activa y se habilita la lista de deseo con sus numeros acttivado
    context={
        'categories': categories,
        'listingAuction': listing,
        'watchlist_count': watchlist.count()
    }
    return render(request, "auctions/index.html", context)

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def createListing(request): 
    if request.method == "POST":
        form = ListingForm(request.POST)
        user = User.objects.get(pk=request.user.id)

        if form.is_valid():

            category = Categories.objects.get(categoryName = form.cleaned_data['category'])

            listing = Auctions(
                titleItem = form.cleaned_data['title'],
                descriptionItem = form.cleaned_data['description'],
                imageItem = form.cleaned_data['image'],
                priceAuction = form.cleaned_data['startingBid'],
                categoryAuction = category,
                userAuction = user
            )
            listing.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createAuction.html", {
                'form': form
            })
    else:
        return render(request, "auctions/createAuction.html",{
        'form': ListingForm()
    })

def searchCategoryAuction(request, category):
    _category = Categories.objects.filter(categoryName = category)
    findCategory = _category[0].id
    listing = Auctions.objects.filter(isActiveAuction=True, categoryAuction = findCategory)
    watchlist = Watchlist.objects.filter(userWatchlist = request.user)
    if listing:
        context={
            'categories': Categories.objects.all(),
            'listingAuction': listing,
            'watchlist_count': watchlist.count()
        }
        return render(request, "auctions/index.html", context)
    else:
        context={
            'categories': Categories.objects.all(),
            'message': "No hay subastas para esta categoria",
            'watchlist_count': watchlist.count()
        }
        return render(request, "auctions/index.html", context)

@login_required
def addWatchlist(request):
    if request.method == 'POST':
        _userWatchlist = request.user
        _auctionWatchlist = Auctions.objects.get(pk=request.POST["idAuction"])

        if Watchlist.objects.filter(userWatchlist = _userWatchlist, auctionWatchlist = _auctionWatchlist):
            print('Ya existe entrada')
        else:
            watchlist = Watchlist(
                userWatchlist = _userWatchlist,
                auctionWatchlist = _auctionWatchlist
            )
            watchlist.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def listWacthlist(request):
    user = User.objects.get(username=request.user)
    watchlist = Watchlist.objects.filter(userWatchlist = user)
    auctions = []
    for i in watchlist:
        print(i.auctionWatchlist.id)
        auctions.append(i.auctionWatchlist.id)
    print(auctions)
    auctionlist = Auctions.objects.filter(pk__in = auctions)
    print(auctionlist)
    return render(request, "auctions/watchlist.html",{
        "watchlist": auctionlist
    }) 

def viewAuction(request, id):
    if request.method == 'GET':
        auction = Auctions.objects.get(id = id)
        context={
            'categories': Categories.objects.all(),
            'auction': auction,
            'watchlist_count': request.user.userWatchlist.all().count()
        }
        return render(request, "auctions/viewAuction.html", context)
    else:
        return HttpResponseRedirect(reverse("index"))
