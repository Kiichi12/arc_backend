from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_folder, name="create_folder"),
    path('delete/<int:id>/', views.delete_folder, name="delete_folder"),
    path('update/<int:id>/', views.rename_folder, name="rename_folder"),
    path('get/<int:id>/', views.get_children, name="get_children")          # can add optional query as ?mime_type=<mime_type>
]