from audioop import maxpp
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Login(AbstractUser):
    mobile_number = models.CharField(max_length=200, unique=True,null=True,blank=True)

class UserType(models.Model):
    LoginType=models.OneToOneField(to=Login, on_delete=models.CASCADE)
    LoginTypeName=models.CharField(max_length=200)#userlogin  #adminlogin

    def __str__(self):
        return self.LoginType.first_name

class LoginProfile(models.Model):
    UserTypeId=models.OneToOneField(to=UserType, on_delete=models.CASCADE)
    ProfilePic=models.ImageField(upload_to="profilepic",null=True, blank=True )
    AlternateMobile=models.CharField(max_length=200,null=True,blank=True)
    Gender=models.CharField(max_length=200,null=True,blank=True)
    DateOfBirth=models.DateField(blank= True,null=True)
    adderess=models.TextField(null=True,blank=True)

class Address(models.Model):
    UserLoginProfileId=models.ForeignKey(to=Login, on_delete=models.CASCADE)
    FullName=models.CharField(max_length=200)
    MobileNo=models.CharField(max_length=200)
    PinCode=models.CharField(max_length=200)
    Address_line1=models.CharField(max_length=200)
    Address_line2=models.CharField(max_length=200)
    Landmark=models.CharField(max_length=200)
    City=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    AddressType=models.IntegerField(default=1)
    AddressStatus=models.BooleanField(default=False)
