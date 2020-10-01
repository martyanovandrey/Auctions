from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist


def index(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
                    "listings": all_listings})


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

def listing(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]       
        description = request.POST["description"]
        url = request.POST["url"]
        try:
            Listings_created = Listing(name=name, price=price, description=description, url=url)
            Listings_created.save()
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })        
    return render(request, "auctions/listing.html")

def active_listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(request, "auctions/active_listing.html", {
        "listing": listing
        })

def watchlist(request):
    curent_user = request.user.id    
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        watchlist = Watchlist(user=curent_user, listing_id=listing_id)
        if Watchlist.objects.filter(user=curent_user, listing_id = listing_id).exists():
            return HttpResponseBadRequest("This item already in your watchlist")
        watchlist.save()
    curent_watchlist = Watchlist.objects.filter(user=curent_user)
    curent_watch_id = curent_watchlist.objects.filter(listing_id=listing_id)
    watch_listing = Listing.objects.filter(id = curent_watch_id)
    return render(request, "auctions/watchlist.html", {
        "all_watchlists": watch_listing
        })
