from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("scrap_race/", views.scrap_race),
    path("download/", views.download),
    path("download_all/", views.download_all),
    path("archive/", views.archive),
]
