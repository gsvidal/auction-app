from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .models import User, AuctionListing, Category, Comment, Watchlist, Bid

def filter_listing_chips(listings, user, used_in):
    watchlist = Watchlist.objects.get(user=user)
    for listing in listings:
        if used_in != "watchlist":
            for item in watchlist.items.all():
                if item.id == listing.id:
                    listing.is_in_watchlist = True
        else:
            listing.is_in_watchlist = True  

    for listing in listings:  
        listing.was_listed_by_user = listing.seller == user
        user_listing_bids = Bid.objects.filter(item=listing, bidder=user)
        has_user_current_bid = False
        if user_listing_bids.count() > 0:
            user_listing_highest_bid = user_listing_bids.order_by('-value').first().value
            has_user_current_bid = user_listing_highest_bid == listing.bid

        listing.has_user_won = not listing.is_active and has_user_current_bid

def index(request):
    listings = AuctionListing.objects.all().order_by('-listing_date')
    threshold_date = timezone.now() - timezone.timedelta(seconds=2.5) 

    for listing in listings:
        listing.is_newly_created = listing.listing_date >= threshold_date

    user = request.user
    if user.username != "":
        filter_listing_chips(listings, user, "index")
               
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": "Active Listings",
    })


def listings(request, listing_id):
    if request.method == "POST":
        text = request.POST["user-comment"]
        author = User.objects.get(pk=int(request.POST["user_id"]))
        item = AuctionListing.objects.get(pk=listing_id)
        if text.strip() != "":
            comment = Comment(text=text, author=author, item=item)
            comment.save()
            return HttpResponseRedirect(reverse("listings", args=[listing_id]))

        messages.warning(request, "Your comment must not be empty")
        return HttpResponseRedirect(reverse("listings", args=[listing_id]))

    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except:
        return render(request, '404.html')
    
    listing_bids = Bid.objects.filter(item=listing)
    
    user = request.user
    if user.username != "":
        listing_in_watchlist = False
        watchlist = Watchlist.objects.get(user=user)
        if watchlist.items.filter(pk=listing_id).exists():
            listing_in_watchlist = True

        is_listing_seller_current_user = listing.seller == user
        user_listing_bids = Bid.objects.filter(item=listing, bidder=user)
        has_user_current_bid = False

        if user_listing_bids.count() > 0:
            user_listing_highest_bid = user_listing_bids.order_by('-value').first().value
            has_user_current_bid = listing.bid == user_listing_highest_bid

        has_user_won = not listing.is_active and has_user_current_bid

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": listing.comments.all().order_by('-date'),
            "listing_in_user_watchlist": listing_in_watchlist,
            "comments_length": listing.comments.all().count(),
            "is_user_current_bid": has_user_current_bid,
            "bids_length": listing_bids.count(),
            "is_seller_current_user": is_listing_seller_current_user,
            "has_user_won": has_user_won
        })
    
    # user not auth
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": listing.comments.all().order_by('-date'),
            "comments_length": listing.comments.all().count(),
            "bids_length": listing_bids.count(),
        })


@login_required
def add_to_watchlist(request, listing_id):
    user = request.user
    item = AuctionListing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.get(user=user)
    
    # Check if the item is already in the user's watchlist
    if not watchlist.items.filter(pk=listing_id).exists():
        watchlist.items.add(item)
        watchlist.save()

    return HttpResponseRedirect(reverse("listings", args=[listing_id]))


@login_required
def remove_from_watchlist(request, listing_id):
    user = request.user
    item = AuctionListing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.get(user=user)

    if watchlist.items.filter(pk=listing_id).exists():
        watchlist.items.remove(item)
        watchlist.save()

    return HttpResponseRedirect(reverse("listings", args=[listing_id]))

@login_required
def watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.get(user=user)
    listings = watchlist.items.all().order_by('-listing_date')

    filter_listing_chips(listings, user, "watchlist")

    return render(request, 'auctions/index.html', {
        "listings": listings,
        "listings_length": listings.count(),
        "title": "Your Watchlist"
    })

def categories(request):
    categories = Category.objects.all().exclude(name="No Listed Category")
    return render(request, 'auctions/categories.html', {
        "categories": categories
    })

def by_categories(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = AuctionListing.objects.filter(category=category).order_by('-listing_date')

    filter_listing_chips(listings, request.user, "by_categories")

    return render(request, 'auctions/index.html', {
        "listings": listings,
        "title": "Category: " + category.name
    })

@login_required
def seller(request, seller_id):
    user_seller = User.objects.get(pk=seller_id)
    listings = AuctionListing.objects.filter(seller=user_seller)

    filter_listing_chips(listings, request.user, "seller")

    return render(request, 'auctions/index.html', {
        "listings": listings,
        "title": "My listings"
    })


@login_required
def bid(request, listing_id):
    if request.method == "POST":
        bid_to_place = request.POST["input_bid"]
        listing_bid = AuctionListing.objects.get(pk=listing_id)
        bids = Bid.objects.filter(item=listing_bid).order_by('-value')
        if listing_bid.is_active:
            try:
                if int(bid_to_place) <= bids.first().value:
                    messages.error(request,"Your bid has to be greater than current bid.")
                    return HttpResponseRedirect(reverse("listings", args=[listing_id]))

                bid = Bid(value=bid_to_place, bidder=request.user, item=listing_bid)
                bid.save()
                listing_bid.bid=bid_to_place
                listing_bid.save()
                listing_bid.current_bidder = request.user
                listing_bid.save()

                messages.success(request,"Your bid has been placed.")
                request.session['bid_message_error'] = ""
                request.session['bid_message_success'] = "Your bid has been placed."
                return HttpResponseRedirect(reverse("listings", args=[listing_id]))

            except ValueError:
                messages.error(request,"You must enter a numeric value")
                return HttpResponseRedirect(reverse("listings", args=[listing_id]))
        return HttpResponseRedirect(reverse("listings", args=[listing_id]))
    

@login_required
def close_listing(request, listing_id):
    listing_to_close = AuctionListing.objects.get(pk=listing_id)
    listing_to_close.is_active = False
    listing_to_close.save()
    messages.info(request,"We're sending a notification to the winner")

    return HttpResponseRedirect(reverse("listings", args=[listing_id]))

@login_required
def delete_listing(request, listing_id):
    listing_to_delete = AuctionListing.objects.get(pk=listing_id)
    listing_to_delete.delete()

    return HttpResponseRedirect(reverse("index"))


@login_required
def create_listing(request):
    if request.method == "POST":
        name = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image_url = request.POST["image_url"] or 'https://i.postimg.cc/gkWVHJNB/no-photo.png'
        category_id = request.POST.get("category")

        if bid.strip() == "" or int(bid) <= 0:
            return render(request, 'auctions/create_listing.html', {
                "message_error": "Bid has to be a positive number"
            })

        # Check if the selected category is 'No Listed Category'
        if category_id == "No Listed Category":
            print("no listed cate")
            category = Category.objects.get_or_create(name="No Listed Category")[0]
        else:
            category = Category.objects.get(pk=int(category_id))

        seller = request.user

        new_listing = AuctionListing(name=name, description=description, bid=int(bid), seller=seller, image_url=image_url, category=category, current_bidder=seller)
        new_listing.save()

        bid = Bid(value=bid, bidder=seller ,item=new_listing)
        bid.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/create_listing.html", {
            "categories": Category.objects.all().exclude(name="No Listed Category").order_by('name')
        })


def login_view(request):
    if request.method == "POST":
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
        if username.strip() == "":
            return render(request, "auctions/register.html", {
                "message": "Username must not be empty"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            watchlist = Watchlist.objects.create(user=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
