from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:id>/", views.add_to_favourites, name="add_to_favourites"),
    path("remove/<int:id>/", views.remove_from_favourites, name="remove_from_favourites"),
    path("get_favourites/<int:id>/<int:floder_id>/<str:mime_type>/<str:sort_by>", views.get_favourites, name="get_favourites")
]

# get_favourites - get all favourites
# get_favourites/<int:id> - get favourites of a user
# get_favourites/<int:id>/<int:folder_id> - get favourites of a user
# get_favourites/<int:id>/<int:folder_id>/<str:mime_type> - get favourites of a user with a specific mime type
# get_favourites/<int:id>/<int:folder_id>/<str:mime_type>/<str:sort_by> - get favourites of a user
# with a specific mime type and sorted by a specific field
# get_favourites/<int:id>/<int:folder_id>/<str:mime_type>/<str:sort_by>/<str:order> - get favourites of a user
# with a specific mime