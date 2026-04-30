from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User,Listing


def index(request):
    listings = Listing.objects.filter(is_active=True) #Get only active listings

    return render(request, "auctions/index.html",{ #Send active listings to the template
        "listings": listings
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

@login_required(login_url="/login") #Only logged-in users can create ads
def create_listing(request): 
    #Save data
    if request.method == "POST": 
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_price = request.POST.get("starting_price")
        image_url = request.POST.get("image_url")
        category = request.POST.get("category")

        listing = Listing.objects.create(
            title=title, 
            description=description,
            starting_price=starting_price,
            image_url=image_url,
            category=category,
            created_by=request.user
        )

        return redirect("index")

    return render(request, "auctions/create_listing.html")