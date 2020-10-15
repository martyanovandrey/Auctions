from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .models import User, Listing, Watchlist, Bid

class Bid_form(forms.Form):
    bid_form = forms.IntegerField(required=True, label='Create your bid')
    bid_form.widget.attrs.update({'class': 'form-control'})

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

def create_listing(request):
    if request.method == "POST":
        name = request.POST["name"]
        starting_bid = request.POST["starting_bid"]       
        description = request.POST["description"]
        url = request.POST["url"]
        owner = request.POST['owner']
        try:
            Listings_created = Listing(name=name, starting_bid=starting_bid, description=description, url=url, owner=owner)
            Listings_created.save()
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "Listing not created."
            })        
    return render(request, "auctions/create_listing.html")

def active_listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        curent_user = request.user.id  
        bid_count = Bid.objects.filter(item_bid=listing_id).count()
        if bid_count > 0:
            max_bid = Bid.objects.filter(item_bid=listing_id).aggregate(Max('bid'))
            max_bid = max_bid['bid__max']
        else:
            max_bid = listing.starting_bid
        if Watchlist.objects.filter(user_watchlist = curent_user, listing_item = listing_id).exists():
            watchlist_state = False
        else:
            watchlist_state = True
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    #Make a Bid block
    if request.method == 'POST':
        #Create form from Bid_form class
        form = Bid_form(request.POST)
        curent_user = request.user.id
        listing_id = request.POST["listing_id"]
        listing_item = Listing.objects.get(id = listing_id)
        user_bid = User.objects.get(id = curent_user)
        if form.is_valid():
            curent_bid = form.cleaned_data['bid_form']
            bid_count = Bid.objects.filter(item_bid=listing_id).count()
            if bid_count > 0:
                max_bid = Bid.objects.filter(item_bid=listing_id).aggregate(Max('bid'))
                max_bid = max_bid['bid__max']
            else:
                max_bid = listing_item.starting_bid
            if curent_bid > max_bid: 
                bid = Bid(user_bid=user_bid, item_bid_id=listing_item.id, bid=curent_bid)
                bid.save()
                return render(request, "auctions/active_listing.html", {
                    "listing": listing_item,
                    'form': Bid_form(),
                    'max_bid': curent_bid,
                    'bid_count': bid_count + 1,
                    "succ_message": f"You made a successful bid for {curent_bid} $ !"
                    })
            else:
                return render(request, "auctions/active_listing.html", {
                    "listing": listing_item,
                    'form': Bid_form(),
                    'max_bid': max_bid,
                    'bid_count': bid_count,                        
                    "err_message": "Bid can't be less than curent max bid"
                    })
        else:           
            return HttpResponseBadRequest("Form is not valid")
    #End bid block
    return render(request, "auctions/active_listing.html", {
        "listing": listing,
        'watchlist_state': watchlist_state,
        'bid_count': bid_count,
        'max_bid': max_bid,
        'form': Bid_form()
        })

def watchlist(request):
    curent_user = request.user.id      
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        # Get User id and Listing id through their models
        watching_user = User.objects.get(id = curent_user)
        listing_item = Listing.objects.get(id = listing_id)
        # Create watchlist
        watchlist = Watchlist(user_watchlist=watching_user, listing_item=listing_item)
        # Check if user already have that item in watchlist
        curent_item = Watchlist.objects.filter(user_watchlist = curent_user, listing_item = listing_item)
        if curent_item.exists():
            curent_item.delete()
        else:
            watchlist.save()
    curent_watch_id = Watchlist.objects.filter(user_watchlist=curent_user)
    curent_watchlist = curent_watch_id.all()
    return render(request, "auctions/watchlist.html", {
        "all_watchlists": curent_watchlist
        })

#@login_required
def close_bid(request, listing_id):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]