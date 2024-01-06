from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path(
        "add_to_watchlist/<int:listing_id>/",
        views.add_to_watchlist,
        name="add_to_watchlist",
    ),
    path(
        "remove_from_watchlist/<int:listing_id>/",
        views.remove_from_watchlist,
        name="remove_from_watchlist",
    ),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("by_categories/<int:category_id>", views.by_categories, name="by_categories"),
    path("seller/<int:seller_id>", views.seller, name="seller"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path(
        "delete_listing/<int:listing_id>", views.delete_listing, name="delete_listing"
    ),
]
