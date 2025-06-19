from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
from .models import File, Tag, FileTags, Comment, FileRating, UserViewed
from django.db.models import Q, Avg, Count

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    serializer = FileUploadSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        file_instance = serializer.save()

        if not file_instance.size:
            file_instance.size = file_instance.file_url.size
            file_instance.save()

        return Response({
            "message": "File uploaded succesfully",
            "file": {
                "id": file_instance.id,
                "name": file_instance.name,
                "url": request.build_absolute_uri(file_instance.file_url.url)
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_files(request, folder_id):
    search_value = request.data.get("search_value", "").strip()
    mime_type = request.data.get("mime_type")

    if not search_value:
        return Response({'files': []}, status=status.HTTP_200_OK)
    
    def get_descendand_folder_ids(parent_id):
        from .models import Folder

        folder_ids = [parent_id]
        queue = [parent_id]

        while queue:
            current_id = queue.pop()
            children = Folder.objects.filter(parent_id=current_id).values_list('id', flat=True)
            folder_ids.extend(children)
            queue.extend(children)
        return folder_ids
    
    folder_ids = get_descendand_folder_ids(parent_id=folder_id)

    if mime_type is None:
        filtered_files = File.objects.filter(
                Q(parent_id__in=folder_ids) &
                (Q(name__icontains=search_value) | Q(filetags__tag__name__icontains=search_value) ) & 
                Q(status='Accepted')
            ).distinct()
    else:
        filtered_files = File.objects.filter(
                Q(parent_id__in=folder_ids) &
                (Q(name__icontains=search_value) | Q(filetags__tag__name__icontains=search_value) ) & 
                Q(status='Accepted') & Q(mime_type=mime_type)
            ).distinct()

    files = []
    for file in filtered_files:
        tags = list(Tag.objects.filter(filetags__file=file).values_list('name', flat=True))
        
        user_rating = FileRating.objects.filter(file=file, user=request.user).first()
        user_rating_value = user_rating.rating if user_rating else None

        avg_rating_data = FileRating.objects.filter(file=file).aggregate(avg_rating=Avg('rating'))
        average_rating = avg_rating_data['avg_rating']

        user_view_count = UserViewed.objects.filter(file=file).aggregate(count=Count('id'))
        user_view_count_value = user_view_count['count']

        files.append({
            "id": file.id,
            "name": file.name,
            "mime_type": file.mime_type,
            "parent": {
                "id": file.parent.id,
                "name": file.parent.name
            } if file.parent else None,
            "created_at": file.created_at,
            "updated_at": file.updated_at,
            "description": file.description,
            "open_count": file.open_count,
            "owner": {
                "id": file.owner.id,
                "username": file.owner.username,
                "email": file.owner.email
            },
            "tags": tags,
            "user_rating": user_rating_value,
            "average_rating": average_rating,
            "url": request.build_absolute_uri(file.file_url.url),
            "user_view_count": user_view_count_value,
        })

    return Response({'files': files}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, id):
    pass

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rename_file(request, id):
    pass

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, id):
    content = request.data.get("comment")

    try:
        file = File.objects.get(id=id)
    except File.DoesNotExist:
        return Response({'error': 'File does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if not content:
        return Response({'error': 'content of the comment is not defined'}, status=status.HTTP_400_BAD_REQUEST)

    comment = Comment.objects.create(user=request.user, file=file, content=content)

    return Response({
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user.id,
        "file_id": comment.file.id
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    comment.delete()
    return Response({'message': 'Comment deleted succesfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_file_comments(request, id):
    try:
        file = File.objects.get(id=id)
    except File.DoesNotExist:
        return Response({'error': 'File does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    comments_data = Comment.objects.filter(file=file)
    comments = [
        {
            "user": {
                "id": comment.user.id,
                "username": comment.user.username,
                "email": comment.user.email
            },
            "file": {
                "id": comment.file.id,
                "name": comment.file.name
            },
            "content": comment.content,
            "commented_at": comment.commented_at
        } for comment in comments_data
    ]
    
    return Response(comments, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_file(request, id):
    rating = request.data.get("rating")

    try:
        file = File.objects.get(id=id)
    except File.DoesNotExist:
        return Response({'error': 'File does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        fileRating = FileRating.objects.get(user=request.user)
        fileRating.rating = rating
        fileRating.save()
    except FileRating.DoesNotExist:
        fileRating = FileRating.objects.create(user=request.user, file=file, rating=rating)

    return Response({
        "id": fileRating.id,
        "rating": fileRating.rating,
        "user_id": fileRating.user.id,
        "file_id": fileRating.file.id
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_viewed(request, id):
    try:
        file = File.objects.get(id=id)
    except File.DoesNotExist:
        return Response({'error': 'File does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    userViewed = UserViewed.objects.create(user=request.user, file=file)

    return Response({
        "id": userViewed.id,
        "user_id": userViewed.user.id,
        "file_id": userViewed.file.id,
        "opened_at": userViewed.opened_at
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_recently_viewed(request):
    try:
        viewed = UserViewed.objects.filter(user=request.user).distinct('file')
    except UserViewed.DoesNotExist:
        return Response([], status=status.HTTP_200_OK)

    userViewed = [
        {
            "id": viewed_file.file.id,
            "name": viewed_file.file.name,
            "url": request.build_absolute_uri(viewed_file.file.file_url.url),
            "mime_type": viewed_file.file.mime_type,
            "size": viewed_file.file.size,
            "description": viewed_file.file.description
        } for viewed_file in viewed
    ]

    return Response(userViewed, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_files(request):
    files = File.objects.filter()

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

    return Response(file_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_file_status(request, id):
    status_value = request.data.get("status")

    if status_value not in ['Accepted', 'Pending', 'Rejected']:
        return Response({'error': 'Invalid status use either of [Accepted, Pending, Rejected]'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        file = File.objects.get(id=id)
    except File.DoesNotExist:
        return Response({'error': 'File does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    file.status = status_value
    file.save()

    user_rating_data = FileRating.objects.filter(user=request.user, file=file).first()
    user_rating = user_rating_data.rating if user_rating_data else None

    avg_rating_data = FileRating.objects.filter(file=file).aggregate(avg_rating=Avg('rating'))
    average_rating = avg_rating_data['avg_rating']

    user_view_count = UserViewed.objects.filter(file=file).aggregate(count=Count('id'))
    user_view_count_value = user_view_count['count']

    return Response({
        "id": file.id,
        "name": file.name,
        "created_at": file.created_at,
        "size": file.size,
        "url": request.build_absolute_uri(file.file_url.url),
        "open_count": file.open_count,
        "mime_type": file.mime_type,
        "user_rating": user_rating,
        "average_rating": average_rating,
        "user_view_count": user_view_count_value,
        "status": file.status
    }, status=status.HTTP_200_OK)

