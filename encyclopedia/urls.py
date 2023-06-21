from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newPage/", views.new_page, name="new_page"),
    path("editPage/", views.edit_page, name="edit_page"),
    path("saveEdit/", views.save_edit, name="save_edit"),
    path("randomPage", views.random_page, name="random_page")
]
