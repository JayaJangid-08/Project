from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USERNAME_FIELD = 'username'
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('manager', 'Manager'), ('member', 'Member')])
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email','role']

    def __str__(self):
        return self.username
