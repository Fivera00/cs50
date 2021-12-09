from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="content"),
    path("newpage/", views.newpage, name="newpage"),
    path("search/", views.search, name="search"),
    path("random/", views.randomPage, name="random"),
    path("edit/<str:title>/", views.editContet, name="edit")

]
