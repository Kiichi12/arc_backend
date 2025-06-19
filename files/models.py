from django.db import models
from users.models import User
from folders.models import Folder
from folders.models import user_directory_path

class File(models.Model):

    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    )

    name = models.CharField(max_length=100)
    file_url = models.FileField(upload_to=user_directory_path)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mime_type = models.CharField(max_length=100)
    size = models.BigIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    open_count = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'files'

class FileRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        db_table = 'file_ratings'
        unique_together = ('user', 'file')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tags'

class FileTags(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'file_tags'
        unique_together = ('file', 'tag')