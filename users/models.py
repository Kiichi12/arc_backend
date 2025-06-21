from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    ROLES = (
        ('guest', 'Guest'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin')
    )

    role = models.CharField(max_length=10, choices=ROLES, default='student')

    class Meta:
        db_table = 'users'
   