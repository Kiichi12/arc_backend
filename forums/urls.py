from django.urls import path
from . import views

urlpatterns =[
    path('create/', views.start_forum, name="start_forum"),
    path('all/', views.get_all_forums, name="get_all_forums"),
    path('user/', views.get_user_forums, name="get_user_forums"),
    path('reply/<int:id>/', views.reply_forum, name="reply_forum"),
    path('get/<int:id>/', views.get_forum, name="get_forum"),
    path('delete/<int:id>/', views.delete_forum, name="delete_forum"),
    path('delete/reply/<int:id>/', views.delete_reply, name="delete_reply"),
]