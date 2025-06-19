from django.db import models
from users.models import User

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