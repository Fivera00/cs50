from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("category/<str:category>/", views.searchCategoryAuction, name="category"),
    path("addwatchlist", views.addWatchlist, name="addwatchlist"),
    path("watchlist", views.listWacthlist, name="watchlist"),
    path("auction/<str:id>/", views.viewAuction, name="auction")

]
