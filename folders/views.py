from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from folders.models import Folder
from files.models import File, FileRating, UserViewed
from django.db.models import Avg, Count

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_folder(request):
    name = request.data.get("name")
    parent_id = request.data.get("parent_id")

    if request.user.role != 'admin':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    if not name:
        return Response({'error': "Folder name is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    name = name.strip()
    parent = None
    if parent_id:
        try:
            parent = Folder.objects.get(id=parent_id)
        except Folder.DoesNotExist:
            return Response({'error': 'Parent folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    folder = Folder.objects.create(name=name, parent=parent, owner=request.user)

    return Response({
        "id": folder.id,
        "name": folder.name,
        "parent_id": folder.parent.id if folder.parent else None,
        "owner_id": folder.owner.id,
        "created_at": folder.created_at,
        "updated_at": folder.updated_at
    }, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_folder(request, id):

    if request.user.role != 'admin':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    if not id:
        return Response({'error': 'Folder id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        folder = Folder.objects.get(id=id, owner=request.user)
    except Folder.DoesNotExist:
        return Response({'error': 'Folder does not exist or is unauthorized'}, status=status.HTTP_404_NOT_FOUND)
    
    folder.delete()

    return Response({"message": "Folder deleted successfully"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rename_folder(request, id):
    name = request.data.get("name")

    if request.user.role != 'admin':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    if not id:
        return Response({'error': 'Folder id is not provided'}, status=status.HTTP_400_BAD_REQUEST)

    if not name:
        return Response({'error': 'New name is not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    name = name.strip()
    try:
        folder = Folder.objects.get(id=id, owner=request.user)
    except Folder.DoesNotExist:
        return Response({"error": "Folder does not exist or is unauthorized"}, status=status.HTTP_404_NOT_FOUND)
    
    folder.name = name
    folder.save()

    return Response({
        "id": folder.id,
        "name": folder.name,
        "parent_id": folder.parent.id if folder.parent else None,
        "owner_id": folder.owner.id,
        "created_at": folder.created_at,
        "updated_at": folder.updated_at
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_children(request, id):

    mime_type = request.query_params.get("mime_type")

    if not id:
        return Response({'error': 'Folder id is not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        folder = Folder.objects.get(id=id)
    except Folder.DoesNotExist:
        return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    subfolders = Folder.objects.filter(parent=folder)
    if mime_type is None:
        files = File.objects.filter(parent=folder, status='Accepted')
    else:
        files = File.objects.filter(parent=folder, status='Accepted', mime_type=mime_type)
        

    subfolder_data = [
        {
            "id": f.id,
            "name": f.name,
            "created_at": f.created_at,
            "updated_at": f.updated_at
        } for f in subfolders
    ]

    file_data = []
    for file in files:
        user_rating_data = FileRating.objects.filter(user=request.user, file=file).first()
        user_rating = user_rating_data.rating if user_rating_data else None

        avg_rating_data = FileRating.objects.filter(file=file).aggregate(avg_rating=Avg('rating'))
        average_rating = avg_rating_data['avg_rating']

        user_view_count = UserViewed.objects.filter(file=file).aggregate(count=Count('id'))
        user_view_count_value = user_view_count['count']
        
        file_data.append({
            "id": file.id,
            "name": file.name,
            "created_at": file.created_at,
            "size": file.size,
            "url": request.build_absolute_uri(file.file_url.url),
            "open_count": file.open_count,
            "mime_type": file.mime_type,
            "user_rating": user_rating,
            "average_rating": average_rating,
            "user_view_count": user_view_count_value
        })

    return Response({
        "folder_id": folder.id,
        "folder_name": folder.name,
        "subfolders": subfolder_data,
        "files": file_data
    }, status=status.HTTP_200_OK)