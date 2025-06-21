from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_report, name="create_report"),
    path('all/', views.get_all_reports, name="get_all_reports"),
    path('user/', views.get_user_reports, name="get_user_reports")
]