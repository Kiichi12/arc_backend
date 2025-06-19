from django.db import models
from users.models import User
from files.models import File

class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        db_table = 'user_reports'
        unique_together = ('user', 'file')
