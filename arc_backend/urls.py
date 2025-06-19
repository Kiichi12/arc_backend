"""
URL configuration for arc_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.conf.urls.static import static

@api_view(["GET"])
def say_hello(request):
    return Response({'message': "Hello world"}, status=200)

urlpatterns = [
    path("", say_hello),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/folders/', include('folders.urls')),
    path('api/forums/', include('forums.urls')),
    path('api/favourites/', include('favourites.urls')),
    path('api/files/', include('files.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
