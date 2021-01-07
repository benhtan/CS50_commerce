from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Watchlist


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

# Django form where user can start a listing
class CreateListingForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=999,widget=forms.Textarea)
    startingBid = forms.DecimalField(label='Starting Bid ($)', min_value=0.00, decimal_places=2, max_digits=99)
    category = forms.CharField(label='Category', required=False, max_length=20)
    imageURL = forms.URLField(label='Image URL', required=False)

@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":

        # Get the form from POST
        form = CreateListingForm(request.POST)

        # Get values from form
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            startingBid = form.cleaned_data['startingBid']
            imageURL = form.cleaned_data['imageURL']
            category = form.cleaned_data['category']
            owner = request.user
            print(owner)
            
            # Insert into database
            l = Listing(title=title, description=description, startingBid=startingBid, imageURL=imageURL, category=category, owner=owner)
            l.save()    

            return HttpResponseRedirect(reverse('listing_page', args=(l.id,)))

        return render(request, 'auctions/create_listing.html', {
            'form': form,
        })
    
    form = CreateListingForm
    return render(request, 'auctions/create_listing.html', {
        "form": form,
    })

def listing_page(request, listingID):

    # Get the listing with matching ID. If not found then go to index.
    try:
        listing = Listing.objects.get(pk=listingID)
    except:
        return HttpResponseRedirect(reverse('index'))

    # Deciding wether the button says Add or Remove from Watchlist
    if request.user.is_authenticated:
        try:
            # Listing is in the watchlist
            watching = Watchlist.objects.get(user=request.user,listing=listing)
            watchlistButtonText = 'Remove from Watchlist'
        
        # Listing is not in watchlist
        except Watchlist.DoesNotExist:
            watchlistButtonText = 'Add to Watchlist'
        except:
            pass

    return render(request, 'auctions/listing_page.html', {
        'listing': listing,
        'watchlistButtonText': watchlistButtonText,
    })

@login_required(login_url='login')
def watchlist(request):
    if request.method == 'POST':
        listingID = request.POST['listingID']
        listing = Listing.objects.get(pk=listingID)

        try:
            # Check if listing is in the Watchlist already.
            # If listing is in Watchlist, then delete.
            w = Watchlist.objects.get(user=request.user,listing=listing)
            w.delete()

        # If listing is not it Watchlist, save it to Watchlist               
        except Watchlist.DoesNotExist:
            watchlist = Watchlist(user=request.user,listing=listing)
            watchlist.save()
        except:
            pass        
        
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))

    return HttpResponseRedirect(reverse("index"))
