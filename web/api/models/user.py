from django.contrib.auth.models import AbstractUser
from django.db import models, connection

class User(AbstractUser):
    yandex_id = models.BigIntegerField(null=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255)
