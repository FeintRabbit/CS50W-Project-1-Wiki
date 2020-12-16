from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/edit/<str:entry>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.rand, name="random"),
]
