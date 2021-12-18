from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("scrap_race/", views.scrap_race),
    path("scrap_races_list/", views.scrap_races_list),
    path("scrap_races_range/", views.scrap_races_range),
    path("download/<str:race_id>/", views.download_csv)
]