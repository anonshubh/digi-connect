from django.db import models
from django.contrib.auth.models import AbstractUser

from allauth.account.signals import email_confirmed
from django.dispatch import receiver

class User(AbstractUser):
    pass

    def __str__(self):
        return self.email


class UserInfo(models.Model):
    """
    Stores the Information About Users
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='info')
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    phone = models.PositiveIntegerField(unique=True)
    department = models.CharField(max_length=56)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_restricted = models.BooleanField(default=False) 

    def __str__(self):
        return f"Info OF {self.user}"
