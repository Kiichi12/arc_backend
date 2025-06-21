from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name="upload_file"),
    path('search/<int:folder_id>/', views.search_files, name="search_files"),
    path('comment/get/<int:id>/', views.get_file_comments, name="get_file_comments"),
    path('comment/add/<int:id>/', views.add_comment, name="add_comment"),
    path('comment/delete/<int:id>/', views.delete_comment, name="delete_comment"),
    path('rate/<int:id>/', views.rate_file, name="rate_file"),
    path('view/<int:id>/', views.add_to_viewed, name="view_file"),
    path('recent/', views.get_user_recently_viewed, name="recently_viewed"),
    path('all/', views.get_all_files, name="get_all_files"),
    path('status/<int:id>/', views.update_file_status, name="update_file_status"),
    path('rename/<int:id>/', views.rename_file, name="rename_file"),
    path('delete/<int:id>/', views.delete_file, name="delete_file"),
]