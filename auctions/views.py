from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max
from django.contrib import messages


from .models import *

@login_required(login_url='/login')
def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all()
    })


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

@login_required(login_url='/login')
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories" : Category.objects.all()
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        price = float(request.POST["starting_bid"])
        url = request.POST["url"]
        categories = request.POST.getlist('categories')
        instance = Listing(title=title, description=description, price=price, img_url=url,active=True, owner=request.user)
        instance.save()
        instance.categories.set(categories)
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def listing(request, listing_id):
    listing=Listing.objects.get(pk=listing_id)
    user=request.user
    messages.success(request, "Congratulations! You got it!")
    comments = listing.comments.all()
    if Bid.objects.filter(listing=listing).all():
        max_price = Bid.objects.filter(listing=listing).all().aggregate(Max('value'))['value__max']
        bid_winner = Bid.objects.get(value=max_price, listing=listing)
        return render(request, "auctions/listing.html", {
            "listing":listing,
            "watchlists":user.listing_on_watchlist.all(),
            "bid_winner":bid_winner,
            "error": "Your bid is the current bid.",
            "categories" : listing.categories.all(),
            "number_of_bids":Bid.objects.filter(listing=listing).all().count(),
            "comments":comments
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing":listing,
            "watchlists":user.listing_on_watchlist.all(),
            "categories" : listing.categories.all(),
            "number_of_bids":Bid.objects.filter(listing=listing).all().count(),
            "comments":comments
        })

@login_required(login_url='/login')
def bid(request, listing_id):
    if request.method == "POST":
        bid = float(request.POST["money"])
        listing =  Listing.objects.get(pk = listing_id)
        user = request.user
        if Bid.objects.filter(listing=listing).all():
            max_price = Bid.objects.filter(listing=listing).all().aggregate(Max('value'))['value__max']
            if bid > max_price:
                bid_object = Bid(value=bid, bid_user=user, listing=listing)
                bid_object.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            else:
                messages.error(request, "The price you put must be higher than the current one!")
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            if bid >= listing.price:
                bid_object = Bid(value=bid, bid_user=user, listing=listing)
                bid_object.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            else:
                messages.error(request, "The price you put must be higher than the current one!")
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required(login_url='/login')
def close(request, listing_id):
    listing =  Listing.objects.get(pk = listing_id)
    listing.active=False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required(login_url='/login')
def watchlist(request):
    if request.method == "GET":
        user = request.user
        return render(request, "auctions/watchlist.html", {
            "listings" : user.listing_on_watchlist.all()
        })
    else:
        id_of = request.POST["listing"]
        listing = Listing.objects.get(pk=id_of)
        user = request.user
        if listing in user.listing_on_watchlist.all():
            listing.watchlist.remove(user)
            listing.save()
        else:
            listing.watchlist.add(user)
            listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required(login_url='/login')
def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listing.objects.get(pk=listing_id)
        object = Comment(content=comment, author=request.user, listing=listing)
        object.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required(login_url='/login')
def categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/categories.html", {
            "categories":categories
        })

@login_required(login_url='/login')
def category(request, category_name):
    if request.method=="GET":
        category=Category.objects.get(name=category_name)
        listings = category.listing.all()
        return render(request, "auctions/category.html", {
            "category":category,
            "listings":listings
        })
