from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all(),
    })


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

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

class CreateListingForm(forms.Form):
    description = forms.CharField(label='Description', max_length=100)
    startingBid = forms.DecimalField(label='Starting Bid ($)', min_value=0.00, decimal_places=2)
    category = forms.CharField(label='Category', required=False, max_length=20)
    imageURL = forms.URLField(label='Image URL', required=False)

@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            description = form.cleaned_data['description']
            startingBid = form.cleaned_data['startingBid']
            imageURL = form.cleaned_data['imageURL']
            category = form.cleaned_data['category']

            l = Listing(description=description, startingBid=startingBid, imageURL=imageURL, category=category)
            l.save()    

            return HttpResponseRedirect(reverse('index'))

        return render(request, 'auctions/create_listing.html', {
            'form': form,
        })
    
    form = CreateListingForm
    return render(request, 'auctions/create_listing.html', {
        "form": form,
    })
