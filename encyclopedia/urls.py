from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    
    path("create-new-page/", views.new_page, name="create-new-page"),

    path("random-page/", views.random_page, name="random-page"),

    path('search/', views.search, name="search"),

    path("wiki/<str:entry>/", views.wiki, name="wiki"),

    path("wiki/<str:entry>/edit/", views.edit_page, name="edit-page"),
]
