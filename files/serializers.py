from rest_framework import serializers
from .models import File, Tag, FileTags

class FileUploadSerializer(serializers.ModelSerializer):

    tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = File
        fields = ['id', 'name', 'file_url', 'parent', 'mime_type', 'size', 'description', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        user = self.context['request'].user
        validated_data['owner'] = user

        file_instance = super().create(validated_data)
        
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name.strip().lower())
            FileTags.objects.create(file=file_instance, tag=tag)
        
        return file_instance