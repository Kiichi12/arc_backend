from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:id>/", views.add_to_favourites, name="add_to_favourites"),
    path("remove/<int:id>/", views.remove_from_favourites, name="remove_from_favourites"),
]