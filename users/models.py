from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True,max_length=255)
    name = models.CharField(max_length=200)
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()
    
    def __str__(self):
        return self.name