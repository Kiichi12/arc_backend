from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from favourites.models import Favourites
from files.models import File

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favourites(request, id):
    try:
        file = File.objects.get(id=id)
    except File.DoesNotExist:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    if Favourites.objects.filter(user=request.user, file=file).exists():
        return Response({'error': 'Already in favourites'}, status=status.HTTP_400_BAD_REQUEST)

    favourite = Favourites.objects.create(user=request.user, file=file)

    return Response({
        "user": {
            "id": favourite.user.id,
            "username": favourite.user.username,
            "email": favourite.user.email
        },
        "file": {
            "name": favourite.file.name,
            "file_url": favourite.file.file_url,
            "mime_type": favourite.file.mime_type,
            "size": favourite.file.size,
            "parent": {
                "id": favourite.file.parent.id,
                "name": favourite.file.parent.name
            },
            "open_count": favourite.file.open_count,
            "description": favourite.file.description,
            "created_at": favourite.file.created_at,
            "updated_at": favourite.file.updated_at
        }
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_favourites(request, id):
    try:
        file = File.objects.get(id=id)
    except File.DoesNotExist:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        favourite = Favourites.objects.get(user=request.user, file=file)
    except Favourites.DoesNotExist:
        return Response({'error': 'Not in favourites'}, status=status.HTTP_404_NOT_FOUND)

    favourite.delete()

    return Response({"message": "Removed from favourites successfully"}, status=status.HTTP_200_OK)
