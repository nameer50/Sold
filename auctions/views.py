
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import New_listing_form, New_Comment_form, New_Bid_form
from .models import Bid, User,Auction,Comment, Watchlist
import os


def index(request):
    CATEGORIES = Auction.Categories
    CATEGORIES = [x[0] for x in CATEGORIES]
    return render(request, "auctions/index.html", {"auctions":Bid.objects.all()})


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


def categories(request, category):
    if request.method == "GET":
        listings = Auction.objects.filter(category=category)
        auctions = []
        for listing in listings:
            auctions.append(Bid.objects.get(listing=listing))

        return render(request, 'auctions/categories.html', {'listings': auctions})


@login_required(login_url="login")
def new_listing(request):
    if request.method == "GET":
        form = New_listing_form()
        return render(request, 'auctions/new_listing.html', {'form':form})
    if request.method == "POST":
        form = New_listing_form(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            img = form.cleaned_data['img']
            discription = form.cleaned_data['discription']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            if category is None:
                category="Other"
            user_post = request.user
            f = Auction(title=title, img=img, discription=discription, price=price, user_post=user_post, category=category)
            f.save()

            # Creating an initial bid with the price the poster provided. This will be used to evaluate new bids
            b = Bid(Bid=price, user_bid=request.user, listing=f)
            b.save()
            w = Watchlist(user_watchlist=request.user, auctions=f)
            w.save()
            messages.success(request, "Listing created successfully!")
            return HttpResponseRedirect(reverse("listing", args=(f.id,)))

        return render(request,"auctions/new_listing.html",{'form':form})
        
def listing(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    comment_form = New_Comment_form()
    comments = Comment.objects.filter(auction=auction)
    bid_form = New_Bid_form()
    bid = Bid.objects.get(listing=auction)
    try:
        on_watchlist = Watchlist.objects.get(user_watchlist=request.user,  auctions=auction)
    except (Watchlist.DoesNotExist, TypeError):
        on_watchlist = None

    return render(request, 'auctions/listing.html', {'auction':auction, 'comment_form':comment_form,
     'comments':comments, 'bid_form':bid_form, 'bid':bid, 'on_watchlist':on_watchlist})

@login_required(login_url="login")
def process_comment(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        form = New_Comment_form(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            if not comment.isspace():
                comment = Comment(comment=comment, user_comment= User.objects.get(pk=request.user.id), auction=auction)
                comment.save()
                messages.success(request, "Commented!")
                return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
            else:
                return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
        else:
            return HttpResponseRedirect(reverse("listing", args=(auction.id,)))

@login_required(login_url="login")
def add_watchlist(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        f = Watchlist(user_watchlist=User.objects.get(pk=request.user.id), auctions=auction)
        f.save()
        messages.success(request, "Added to watchlist!")
        return HttpResponseRedirect(reverse("listing", args=(auction.id,)))

@login_required(login_url="login")
def remove_watchlist(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        f = Watchlist.objects.get(user_watchlist=request.user, auctions=auction)
        f.delete()
        messages.success(request, "Removed from watchlist!")
        return HttpResponseRedirect(reverse("listing", args=(auction.id,)))

@login_required(login_url="login")
def make_bid(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        form = New_Bid_form(request.POST)
        user = request.user

        # Dont want to allow the poster to bid on their own listing. That is corruption.
        if auction.user_post == request.user:
            return HttpResponse("Cannot bid on your own listing")

        # Here I am checking if the current bid in the database is higher or lower than the provided bid
        # I am deleting a bid from the database if the provided bid is higher than the one there and storing the new one.    
        if form.is_valid():
            bid = form.cleaned_data["Bid"]
            bids = Bid.objects.get(listing=auction)
            highest_bid = bids.Bid
            if bid <= highest_bid:
                messages.error(request, "Bid must be higher than the current highest bid")
                return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
            else:
                bids.delete()
                b = Bid(Bid=bid, user_bid=user, listing=auction)
                b.save()
                try:
                    exists = Watchlist.objects.get(user_watchlist=request.user,auctions=auction)
                except Watchlist.DoesNotExist:
                    exists = None
                if exists is None:
                    f = Watchlist(user_watchlist=request.user, auctions=auction)
                    f.save()
                    

                messages.success(request, "Bid made")
                return HttpResponseRedirect(reverse("listing", args=(auction.id,)))

def close_listing(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        auction.active = False
        auction.save()
        messages.success(request, "Listing is closed")
        return HttpResponseRedirect(reverse("listing", args=(auction.id,)))

@login_required(login_url="login")
def watchlist(request):
    if request.method == "GET":
        user = User.objects.get(pk=request.user.id)
        watchlist = user.user_watch.all()
        bid = []
        for listings in watchlist:
            bid.append(Bid.objects.get(listing=listings.auctions))

        return render(request, 'auctions/watchlist.html', {'watchlist': bid})


