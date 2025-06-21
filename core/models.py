from django.db import models
from users.models import User

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

