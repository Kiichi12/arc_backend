from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('user/<int:id>/', views.user_view),
    path('user/update/<int:id>/', views.update_user_view),
]