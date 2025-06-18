from django.db import models
from users.models import User

class Folder(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'folders'

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

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

class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        db_table = 'user_reports'
        unique_together = ('user', 'file')

class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favourites'
        unique_together = ('user', 'file')

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

class Forum(models.Model):
    started_by = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    topic = models.TextField()

    class Meta:
        db_table = 'forums'

class Reply(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'replies'

class LoginLog(models.Model):
    STATUS_CHOICES = (
        ('Failed', 'Failed'),
        ('Sucess', 'Success')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    login_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'login_logs'

