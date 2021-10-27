from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="content"),
    path("newpage", views.newpage, name="newpage")
]
