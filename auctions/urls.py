from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<str:auction_id>", views.listing, name="listing"),
    path("process_comment/<str:auction_id>", views.process_comment, name="process_comment"),
    path("add_watchlist/<str:auction_id>", views.add_watchlist, name="add_watchlist"),
    path("make_bid/<str:auction_id>", views.make_bid, name="make_bid"),
    path("remove_watchlist/<str:auction_id>", views.remove_watchlist, name="removeWatchlist"),
    path("close_listing/<str:auction_id>", views.close_listing, name="close_listing")
]
