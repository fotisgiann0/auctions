from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CommentsForm, BidForm

from .models import User, Listing, Comments, Watchlist, Bid, ClosedListing


def index(request):
    closed = ClosedListing.objects.all()
    closed_listings = [c.item.title for c in closed]
    listing = Listing.objects.exclude(title__in=closed_listings).all()
    return render(request, "auctions/index.html", {
        "listings": listing,
        "comments": Comments.objects.all()
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

def add_listing(request):
    return render(request, "auctions/add_listing.html")

def add_item(request):
    if request.method == "POST":
        # Attempt to add item
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"] 
        category = request.POST["category"]
        image_url = request.POST["image_url"]
        new_item = Listing(listing_by = request.user, title=title, description=description, starting_bid=starting_bid, category=category, image=image_url)
        new_item.save()
        return HttpResponseRedirect(reverse("index"))

def listing_page(request, title):
    listing = Listing.objects.get(title=title)
    if request.user.is_authenticated:
        watch1 = Watchlist.objects.filter(user=request.user, item=listing).first()
        user1 = request.user
    else:
        watch1 = None
        user1 = None
    closed = ClosedListing.objects.filter(item=listing).all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": Comments.objects.filter(on_item=listing).all(),
        "bids": Bid.objects.filter(item=listing).all(),
        "user": user1,
        "watchlist": watch1,
        "form": CommentsForm(),
        "second_form": BidForm(),
        "closed": closed.first()
    }) 

@login_required(login_url='login')
def watch(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user=request.user),
        "comments": Comments.objects.all()
    })
@login_required(login_url='login')
def add_to_list(request, title): #adds or removes from watchlist
    listing = Listing.objects.get(title=title)
    check = Watchlist.objects.filter(user=request.user, item=listing).first()
    if check is not None:
        check.delete()
    else:
        check = Watchlist(user=request.user, item=listing)
        check.save()
    return HttpResponseRedirect(reverse("listing_page", args=[title]))



@login_required(login_url='login')
def get_comment(request, title):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CommentsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            listing = Listing.objects.get(title=title)
            comment = form.cleaned_data["comment"]
            # process the data in form.cleaned_data as required
            new_comment = Comments(on_item=listing, comment=comment, comment_by=request.user)
            new_comment.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("listing_page", args=[title]))
        else:
            return HttpResponseRedirect(reverse("index"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentsForm()

    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def get_bid(request, title):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = BidForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            listing = Listing.objects.get(title=title)
            bid = form.cleaned_data["bid"]
            if bid >= listing.starting_bid:
                for b in Bid.objects.filter(item=listing).all():
                    if b.price > bid:
                        return render(request, "auctions/error.html", {
                            "message": "bid must be greater than current bids"
                        }) 
                else:       
                    new_bid = Bid(item=listing, price=bid, bid_by=request.user)
                    new_bid.save()
                return HttpResponseRedirect(reverse("listing_page", args=[title]))
            else:
                return render(request, "auctions/error.html", {
                            "message": "bid must be greater than starting bid"
                         })
        else:
            return render(request, "auctions/error.html", {
                            "message": "problem with form"
                        }) 


    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url='login')
def close_listing(request, title): 
    listing = Listing.objects.get(title=title)
    max_price = listing.starting_bid
    for b in Bid.objects.filter(item=listing).all():
        if b.price > max_price:
            max_price = b.price
            user = b.bid_by
    closed = ClosedListing(item=listing, winner=user)
    closed.save()
    return HttpResponseRedirect(reverse("index"))

def category(request): 
    listing = Listing.objects.all()
    cat = [l.category for l in listing]
    myset = set(cat)
    categories = list(myset)
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_filter(request, cat): 
    listing = Listing.objects.filter(category=cat)
    return render(request, "auctions/index.html", {
        "listings": listing,
        "comments": Comments.objects.all()
    })

