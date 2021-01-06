from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    description = models.CharField(max_length=100)
    startingBid = models.DecimalField(decimal_places=2, max_digits=99)
    category = models.CharField(max_length=100)
    imageURL = models.URLField(max_length=999)
    