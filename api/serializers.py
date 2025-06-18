from rest_framework import serializers
from core.models import File, Folder

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('owner', 'status', 'open_count', 'mime_type', 'size')
    
    def create(self, validated_data):
        file_obj = validated_data['file_url']
        validated_data['mime_type'] = file_obj.content_type
        validated_data['size'] = file_obj.size
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
        read_only_fields = ('owner',)