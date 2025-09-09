from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.backends import BaseUserManager
# Create your models here.

class Book(models.model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True,blank=True)
    profile_photo = models.ImageField(null=True,blank=True)
    
    
class CustomUserManager(BaseUserManager):
    def create_user(self,request,username=None,password=None):
        if not username:
            raise ValueError("Username required")
        
    def create_superuser(self,request,username=None,password=None):
        if not username:
            raise ValueError("Username required")
