from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import New_listing_form, New_Comment_form, New_Bid_form
from .models import Bid, User,Auction,Comment, Watchlist
import os


def index(request):
    return render(request, "auctions/index.html", {"auctions":Auction.objects.all()})


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

def categories(request):
    return HttpResponse("categories")






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
            user_post = request.user
            f = Auction(title=title, img=img, discription=discription, price=price, user_post=user_post)
            f.save()
            b = Bid(Bid=price, user_bid=request.user, listing=f)
            b.save()

            return HttpResponse("success")

        return render(request,"auctions/new_listing.html",{'form':form})
        
def listing(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    comment_form = New_Comment_form()
    comments = Comment.objects.filter(auction=auction)
    bid_form = New_Bid_form()
    return render(request, 'auctions/listing.html', {'auction':auction, 'comment_form':comment_form, 'comments':comments, 'bid_form':bid_form})

def process_comment(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        form = New_Comment_form(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            comment = Comment(comment=comment, user_comment= User.objects.get(pk=request.user.id), auction=auction)
            comment.save()
            return HttpResponse("commented")

def add_watchlist(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        f = Watchlist(user_watchlist=User.objects.get(pk=request.user.id), auctions=auction)
        f.save()
        return HttpResponse("added to watchlist")

def make_bid(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        form = New_Bid_form(request.POST)
        user = request.user
        if auction.user_post == request.user:
            return HttpResponse("Cannot bid on your own listing")
        if form.is_valid():
            bid = form.cleaned_data["Bid"]
            bids = Bid.objects.get(listing=auction)
            highest_bid = bids.Bid
            if bid <= highest_bid:
                return HttpResponse("Bid must be higher than the current highest bid")
            else:
                bids.delete()
                b = Bid(Bid=bid, user_bid=user, listing=auction)
                b.save()
                return HttpResponse("Bid made")

@login_required()
def watchlist(request):
    if request.method == "GET":
        user = User.objects.get(pk=request.user.id)
        return render(request, 'auctions/watchlist.html', {'watchlist': user.user_watch.all()})


