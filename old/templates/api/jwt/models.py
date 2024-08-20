from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

# Create your models here


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    username = models.TextField(max_length=42, unique=True)
    is_superuser = models.BooleanField(default=False)
    # Other details here

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
