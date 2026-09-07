import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username







