from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/<int:categories>", views.categories, name="categories"),
    path("insertgames", views.createGame, name="createGame"),
    path("games", views.games, name="games"),
    path("deletegames/<int:game>", views.deleteGame, name="deleteGame"),

   #Api urls
    path("api/games", views.getGames, name="getgames"),
    path("api/categories", views.getCategories, name="getcategories"),
    path("api/challenges", views.getChallenges, name="getchallenges"),
    path("api/category/<int:category>/challenges", views.getChallengesByCategory, name="getchallengesbycategory"),
    path("api/game/<int:game>/challenges", views.getChallengesByGame, name="getchallengesbygame"),
    path("api/game/<int:game>/category/<int:category>/challenges", views.getChallengesByGameAndCategory, name="getchallengesbygameandcategory"),

]
