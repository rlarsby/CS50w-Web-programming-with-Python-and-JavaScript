from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name="page"),
    path("results", views.results, name="results"),
    path("new", views.new, name="new"),
    path("wiki/<str:name>/edit", views.edit, name="edit"),
    path("random", views.random, name="random")
]

