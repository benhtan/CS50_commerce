from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listingID>", views.listing_page, name="listing_page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.selectCategory, name="selectCategory"),
    path("listing/<int:listingID>/bid", views.bid, name="bid"),
    path("listing/<int:listingID>/close", views.close_listing, name="close_listing"),
    path("listing/<int:listingID>/comment", views.comment, name="comment"),
]
