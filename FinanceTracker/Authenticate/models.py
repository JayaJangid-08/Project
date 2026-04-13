from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # id = models.AutoField(primary_key=True)
    USERNAME_FIELD = 'username'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
