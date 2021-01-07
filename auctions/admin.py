from django.contrib import admin
from .models import User, Listing, Watchlist
from django import forms

from django.db import models
#from auctions.models import MyModel
#from auctions.widgets import RichTextEditorWidget

# Register your models here.
class ListingModelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', "description", 'startingBid', 'category', 'owner', 'imageURL')
    form = ListingModelForm

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)