from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from forums.models import Forum, Reply

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_forum(request):
    topic = request.data.get("topic")

    if not topic:
        return Response({'error': 'Topic is required to start a forum'}, status=status.HTTP_400_BAD_REQUEST)
    
    forum = Forum.objects.create(topic=topic, started_by=request.user)

    return Response({
        "id": forum.id,
        "started_at": forum.started_at,
        "topic": forum.topic,
        "started_by": {
            "id": forum.started_by.id,
            "username": forum.started_by.username,
            "email": forum.started_by.email
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_forums(request):
    forums = Forum.objects.filter(started_by=request.user)

    forums_data = [
        {
            "id": forum.id,
            "topic": forum.topic,
            "started_at": forum.started_at
        } for forum in forums
    ]

    return Response(forums_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_forum(request, id):
    content = request.data.get("content")

    if not content:
        return Response({'error': 'Content is required to reply a forum'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        forum = Forum.objects.get(id=id)
    except Forum.DoesNotExist:
        return Response({'error': 'Forum does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    reply = Reply.objects.create(content=content, forum_id=id, posted_by=request.user)

    return Response({
        "id": reply.id,
        "content": reply.content,
        "forum_id": reply.forum.id,
        "posted_by": {
            "id": reply.posted_by.id,
            "username": reply.posted_by.username,
            "email": reply.posted_by.email
        }
    }, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forum(request, id):
    try:
        forum = Forum.objects.get(id=id)
    except Forum.DoesNotExist:
        return Response({"error": "Forum does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    replies = Reply.objects.filter(forum=forum)
    reply_data = [
        {
            "id": reply.id,
            "content": reply.content,
            "posted_at": reply.posted_at,
            "posted_by": {
                "id": reply.posted_by.id,
                "username": reply.posted_by.username,
                "email": reply.posted_by.email
            }
        } for reply in replies
    ]

    return Response({
        "id": forum.id,
        "topic": forum.topic,
        "started_by": {
            "id": forum.started_by.id,
            "username": forum.started_by.username,
            "email": forum.started_by.email
        },
        "started_at": forum.started_at,
        "replies": reply_data
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_forum(request, id):
    try:
        forum = Forum.objects.get(id=id, started_by=request.user)
    except Forum.DoesNotExist:
        return Response({'error': 'Forum not found'}, status=status.HTTP_404_NOT_FOUND)
    
    forum.delete()

    return Response({'message': 'forum succesfully deleted'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reply(request, id):
    try:
        reply = Reply.objects.get(id=id, posted_by=request.user)
    except Reply.DoesNotExist:
        return Response({'error': 'Reply not found'}, status=status.HTTP_404_NOT_FOUND)
    
    reply.delete()

    return Response({'message': 'reply succesfully deleted'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_forums(request):
    
    forums = Forum.objects.filter().order_by('-started_at')

    forum_data = []
    for forum in forums:
        forum_data.append({
            "id": forum.id,
            "topic": forum.topic,
            "started_by": {
                "id": forum.started_by.id,
                "username": forum.started_by.username,
                "email": forum.started_by.email
            },
            "started_at": forum.started_at
        })

    return Response(forum_data, status=status.HTTP_200_OK)