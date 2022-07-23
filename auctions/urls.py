from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
<<<<<<< HEAD
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist")
=======
    path("register", views.register, name="register")
>>>>>>> b6775d96e03aefe96f4ee210ea38eb5035e1343c
]
