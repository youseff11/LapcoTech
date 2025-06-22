# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email'] 

    def __str__(self):
        return self.username