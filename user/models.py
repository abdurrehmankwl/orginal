from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  
    username = models.CharField(max_length=150, unique=True)  
    password = models.CharField(max_length=128)  

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

   
    USERNAME_FIELD = "username"  

    def __str__(self):
        return self.username
