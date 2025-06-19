from django.db import models
from users.models import User
from files.models import File

class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favourites'
        unique_together = ('user', 'file')
