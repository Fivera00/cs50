
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("post", views.save_update_post, name="post"),
    path("like/<int:postId>", views.likeDislike, name="likeDislike")
    
]
