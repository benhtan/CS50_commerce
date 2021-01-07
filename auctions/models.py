from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.id} {self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=100, default = "")
    description = models.CharField(max_length=999)
    startingBid = models.DecimalField(decimal_places=2, max_digits=99)
    category = models.CharField(max_length=20, blank=True)
    imageURL = models.URLField(max_length=99999, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userListings')
    creationDate = models.DateTimeField(auto_now_add=True)
    maxBid = models.ForeignKey('Bid', on_delete=models.CASCADE, blank=True, null=True, related_name='maxBid_rev')

    def __str__(self):
        return f"{self.id} {self.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userWatchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userBid')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listingBids')
    userBid = models.DecimalField(decimal_places=2, max_digits=99)
    bidDateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.user} {self.listing} {self.userBid}"