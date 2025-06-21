from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from core.models import File, Folder
from api.serializers import FileSerializer, FolderSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return File.objects.all()
        return File.objects.filter(status='Accepted')
    
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permissions_classes = [permissions.IsAuthenticated]
