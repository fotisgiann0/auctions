from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("add_item", views.add_item, name="add_item"),
    path("listing_page/<title>", views.listing_page, name="listing_page"),
    path("watchlist", views.watch, name="watch"),
    path("add_to_list/<title>", views.add_to_list, name="add_to_list"),
    path("get_comment/<title>", views.get_comment, name="get_comment"),
    path("get_bid/<title>", views.get_bid, name="get_bid"),
    path("close_listing/<title>", views.close_listing, name="close_listing"),
    path("category", views.category, name="category"),
    path("categories/<cat>", views.category_filter, name="category_filter")
]
