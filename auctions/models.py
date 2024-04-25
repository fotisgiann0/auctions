from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    image = models.URLField()
    starting_bid = models.FloatField()
    listing_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="listing_by",  related_name="listing_by_user")

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product")
    price = models.FloatField()
    bid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="bid_by", related_name="bid_by_user")

class Comments(models.Model):
    on_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="on_product")
    comment = models.CharField(max_length=120)
    comment_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="comment_by", related_name="comment_by_user")

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_column="by_user", on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, db_column="listing_by", related_name="watch_listing")

class ClosedListing(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, db_column="by_user", on_delete=models.CASCADE)