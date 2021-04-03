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

    def __str__(self):
        return f"Info Of {self.user}"



# @receiver(email_confirmed)
# def user_info_creation(request,email_address,**kwargs):
#     user = email_address.user
#     print(kwargs)
#     # email = user.email
#     # index = email.find('@')
#     # dot = email.find('.')
#     # domain = email[index+1:dot]
#     # if(domain == 'iiitdm'):
#     #     inst_obj = Institute.objects.get(domain=domain)
#     #     department = email[:3]
#     #     year = email[3:5]
#     #     year_ = "20"+year
#     #     if(year=="19"):
#     #         if(department=='mfd' or department=='mpd' or department=='mdm'):
#     #             department="mdm/mpd/mfd"
#     #         elif(department=='coe' or department=='ced'):
#     #             department="coe/ced"
#     #         elif(department=='edm' or department=='evd' or department=='esd'):
#     #             department="edm/evd/esd"
#     #Addition or selection of another Institute will be in 'else' clause 

#     # user_obj = UserInfo.objects.create(
#     #     user=user,
#     # )


