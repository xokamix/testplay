from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend the built-in User model
class lpUserUser(AbstractUser):
    # Extend the base class with additional fields if necessary
    pass

class Teacher(models.Model):
    user = models.OneToOneField(lpUserUser, on_delete=models.CASCADE)
    subjects_taught = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class Pupil(models.Model):
    user = models.OneToOneField(lpUserUser, on_delete=models.CASCADE)
    # Add pupil-specific fields here

    def __str__(self):
        return self.user.username

class Administrator(models.Model):
    user = models.OneToOneField(lpUserUser, on_delete=models.CASCADE)
    # Add administrator-specific fields here

    def __str__(self):
        return self.user.username
