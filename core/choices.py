from django.db import models

class Role (models.TextChoices):
    GUEST = 'guest', 'Guest'
    STUDENT = 'student', 'Student'
    FACULTY = 'faculty', 'Faculty'
    ADMIN = 'admin', 'Admin'

class LoginStatus (models.TextChoices):
    FAILED = 'Failed', 'Failed'
    SUCCESS = 'Success', 'Success'

class StatusType (models.TextChoices):
    ACCEPTED = 'Accepted', 'Accepted'
    REJECTED = 'Rejected', 'Rejected'
    PENDING = 'Pending', 'Pending'