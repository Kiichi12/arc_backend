from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from reports.models import Report
from users.models import User
from files.models import File
from .utils import ReportPagination

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_report(request):
    content = request.data.get("content")
    file_id = request.data.get("file_id")

    if not content:
        return Response({'error': 'Content is required to report'}, status=status.HTTP_400_BAD_REQUEST)
    if not file_id or not user_id:
        return Response({'error': 'File ID and User ID are required to report'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return Response({'error': 'File does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    report = Report.objects.create(
        content=content,
        file=file,
        reported_by=request.user,
    )
    return Response({
        "id": report.id,
        "content": report.content,
        "file_id": report.file_id,
        "reported_by": report.reported_by.id,
        "created_at": report.created_at
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_reports(request):
    if request.user.role != 'admin':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    reports = Report.objects.filter().order_by('-created_at')

    result_page = ReportPagination().paginate_queryset(reports, request)
    reports_data = []
    for report in reports:
        reports_data.append({
            "id": report.id,
            "content": report.content,
            "file_id": report.file.id,
            "reported_by": {
                "id": report.reported_by.id,
                "username": report.reported_by.username,
                "email": report.reported_by.email
            },
            "created_at": report.created_at
        })
    return Response(ReportPagination().get_paginated_response(reports_data), status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_reports(request):
    reports = Report.objects.filter(reported_by=request.user)
    reports_data = []
    for report in reports:
        reports_data.append({
            "id": report.id,
            "content": report.content,
            "file_id": report.file.id,
            "reported_by": {
                "id": report.reported_by.id,
                "username": report.reported_by.username,
                "email": report.reported_by.email
            },
            "created_at": report.created_at
        })
    return Response(reports_data, status=status.HTTP_200_OK)

