from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import NON_FIELD_ERRORS
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
        
    #Si hay usuario logueado, se muestra la lista activa y se habilita la lista de deseo con sus numeros acttivado
    context={
        'categories': categories,
        'listingAuction': listing,
        'watchlist_count': request.user.userWatchlist.all().count()
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
        'categories': Categories.objects.all(),
        'form': ListingForm(),
        'watchlist_count': request.user.userWatchlist.all().count()
    })

def searchCategoryAuction(request, category):
    _category = Categories.objects.filter(categoryName = category)
    listing = Auctions.objects.filter(isActiveAuction=True, categoryAuction__in = _category)
    if request.user.id is None:
        if listing:
            context={
                'categories': Categories.objects.all(),
                'listingAuction': listing
            }
            return render(request, "auctions/index.html", context)
        else:
            context={
                'categories': Categories.objects.all(),
                'message': "There aren't auctions in this category!!!"
            }
            return render(request, "auctions/index.html", context)
    if listing:
        context={
            'categories': Categories.objects.all(),
            'listingAuction': listing,
            'watchlist_count': request.user.userWatchlist.all().count()
        }
        return render(request, "auctions/index.html", context)
    else:
        context={
            'categories': Categories.objects.all(),
            'message': "There aren't auctions in this category!!!",
            'watchlist_count': request.user.userWatchlist.all().count()
        }
        return render(request, "auctions/index.html", context)

@login_required
def addWatchlist(request):
    if request.method == 'POST':
        _userWatchlist = request.user
        _auctionWatchlist = Auctions.objects.get(pk=request.POST["idAuction"])
        if Watchlist.objects.filter(userWatchlist = _userWatchlist, auctionWatchlist = _auctionWatchlist):
            _userWatchlist.userWatchlist.filter(auctionWatchlist = _auctionWatchlist).delete()
            return HttpResponseRedirect(reverse("index"))
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
    # print(user.userWatchlist.exists())
    return render(request, "auctions/watchlist.html", {
        'categories': Categories.objects.all(),
        'watchlist': user.userWatchlist.all(),
        'watchlist_count': request.user.userWatchlist.all().count()
    })

@login_required
def viewAuction(request, idAuction):
    validAuction = Auctions.objects.filter(id = idAuction)
    auction = Auctions.objects.get(id = idAuction)
    currentBid = 0
    try:
        bid = Bid.objects.filter(auctionBid = idAuction).last()
        currentBid = bid.bidPrice
        print(bid)
    except:
        currentBid = auction.priceAuction
    if request.method == 'GET':
        allComment = Comments.objects.filter(auctionComment = auction)
        if validAuction:
            context={
                'categories': Categories.objects.all(),
                'auction': auction,
                'watchlist_count': request.user.userWatchlist.all().count(),
                'currentBid': currentBid,
                'comments': allComment
            }
            return render(request, "auctions/viewAuction.html", context)
        else:
            print("No existe la subasta")
            return HttpResponseRedirect(reverse("index"))
    else:
        _bid = request.POST["bid"]
        _commment = request.POST["comment"]
        if int(_bid) > currentBid:
            userBid = Bid(
                bidPrice = _bid,
                userBid = request.user,
                auctionBid = auction
            )
            userBid.save()
            if _commment != "":
                auctionCommet = Comments(
                    comment = _commment,
                    userComment = request.user,
                    auctionComment = auction
                )
                auctionCommet.save()                
        else:
            context={
                'categories': Categories.objects.all(),
                'auction': auction,
                'watchlist_count': request.user.userWatchlist.all().count(),
                'currentBid': currentBid,
                'message': "Your bid is lower than the current bid"
            }
            return render(request, "auctions/viewAuction.html", context)
        
        return HttpResponseRedirect(reverse('auction', args=(idAuction)))
