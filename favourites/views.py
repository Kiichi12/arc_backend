from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from favourites.models import Favourites
from files.models import File
from users.models import User

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favourites(request, id, folder_id=None, file_type=None, sort_by=None):
    # try:
    #     user = User.get(id=id)
    # except File.DoesNotExist:
    #     return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    favourites = Favourites.objects.filter(user=user)
    if folder_id:
        favourites = favourites.filter(file__parent__id=folder_id)
    
    if file_type:
        favourites = favourites.filter(file__mime_type=file_type)
    if sort_by:
        if sort_by == 'name':
            favourites = favourites.order_by('file__name')
        elif sort_by == 'size':
            favourites = favourites.order_by('file__size')
        elif sort_by == 'created_at':
            favourites = favourites.order_by('file__created_at')
        elif sort_by == 'updated_at':
            favourites = favourites.order_by('file__updated_at')
        else:
            return Response({'error': 'Invalid sort option'}, status=status.HTTP_400_BAD_REQUEST)

    if not favourites.exists():
        return Response({'message': 'No favourites found'}, status=status.HTTP_404_NOT_FOUND)

    favourite_files = []
    for favourite in favourites:
        fabourite_files.append({
            "user": {
                "id": favourite.user.id,
                "username": favourite.user.username,
                "email": favourite.user.email
            },
            "file": {
                "id": favourite.file.id,
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
        })

    return Response(favourite_files, status=status.HTTP_200_OK)
    