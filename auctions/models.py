from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import pytz

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass
    def __str__(self):
        return f"id: {self.id}, username:{self.username}, email: {self.email}"  

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"id: {self.id}, name:{self.name}"  

class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    bid = models.IntegerField()
    listing_date = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items_listed')
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    # optional attributes:
    image_url = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items_by_category')
 
    def __str__(self):
        return f"id: {self.id}, Name: {self.name}, Description: {self.description}, Starting Bid: ${self.bid}, Listing Date: {self.listing_date}, Seller: {self.seller.username}, Is Active: {self.is_active}, Category: {self.category.name}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=400)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    value = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    items = models.ManyToManyField(AuctionListing, related_name='watchlists')

    def __str__(self):
        return f"id: {self.id}, user: {self.user}, items: {self.items}"